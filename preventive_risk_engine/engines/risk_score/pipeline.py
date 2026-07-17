"""
End-to-end scoring pipeline -- a direct implementation of Appendix B's
pseudocode:

  1. Red-flag override check -> short-circuit to CRITICAL/EMERGENCY if fired.
  2. Eight sub-score calculators (each 0-100, wraps a validated instrument).
  3. Weighted aggregation, renormalized over present data.
  4. Data completeness / confidence.
  5. Explanation engine (top-5 drivers).
  6. Intervention + escalation mapping.
  7. (Audit logging is left to the caller/service layer in this package --
     see docs/architecture.md -- to keep this pure and easily unit-testable.)
"""

from typing import Any

from preventive_risk_engine.enums.risk_level import RiskLevel, DataConfidence
from preventive_risk_engine.models.risk_result import RiskResult, SubScoreResult

from preventive_risk_engine.engines.risk_score.calculators.acute_calculator import AcuteDeteriorationCalculator
from preventive_risk_engine.engines.risk_score.calculators.chronic_calculator import ChronicBurdenCalculator
from preventive_risk_engine.engines.risk_score.calculators.readmission_calculator import ReadmissionCalculator
from preventive_risk_engine.engines.risk_score.calculators.medication_calculator import MedicationRiskCalculator
from preventive_risk_engine.engines.risk_score.calculators.adherence_calculator import AdherenceCalculator
from preventive_risk_engine.engines.risk_score.calculators.lifestyle_calculator import LifestyleSocialCalculator
from preventive_risk_engine.engines.risk_score.calculators.care_gap_calculator import CareGapCalculator
from preventive_risk_engine.engines.risk_score.calculators.preventive_calculator import PreventiveCareCalculator

from preventive_risk_engine.engines.risk_score.red_flag_engine import RedFlagEngine
from preventive_risk_engine.engines.risk_score.aggregator import WeightedAggregator
from preventive_risk_engine.engines.risk_score.explanation_engine import ExplanationEngine
from preventive_risk_engine.engines.risk_score.intervention_engine import InterventionEngine
from preventive_risk_engine.engines.risk_score.escalation_engine import EscalationEngine

from preventive_risk_engine.exceptions.calculator_exception import CalculatorError


class RiskScorePipeline:
    def __init__(self, config: Any):
        self.config = config
        self.red_flag_engine = RedFlagEngine(config)
        self.aggregator = WeightedAggregator()
        self.explanation_engine = ExplanationEngine(config)
        self.intervention_engine = InterventionEngine()
        self.escalation_engine = EscalationEngine()

        self.calculators = [
            AcuteDeteriorationCalculator(config),
            ChronicBurdenCalculator(config),
            ReadmissionCalculator(config),
            MedicationRiskCalculator(config),
            AdherenceCalculator(config),
            LifestyleSocialCalculator(config),
            CareGapCalculator(config),
            PreventiveCareCalculator(config),
        ]

    def run(self, patient: Any) -> RiskResult:
        locale_value = patient.locale.value if hasattr(patient.locale, "value") else str(patient.locale)
        result = RiskResult(
            patient_id=patient.patient_id,
            rules_version=self.config.version,
            locale=locale_value,
        )

        # 1. Red-flag override check.
        red_flags = self.red_flag_engine.check(patient)
        if red_flags:
            result.red_flag = True
            result.red_flags = red_flags
            result.risk_level = RiskLevel.CRITICAL
            result.escalation_level = self.escalation_engine.escalation_tier(
                RiskLevel.CRITICAL, {}, patient, red_flags
            )
            result.data_confidence = DataConfidence.from_completeness(
                self._completeness(patient)
            )
            result.completeness_pct = self._completeness(patient)
            return result

        # 2. Eight sub-score calculators.
        raw_values = {}
        for calc in self.calculators:
            try:
                value = calc.compute(patient)
            except CalculatorError:
                value = None  # safe failure: excluded, never coerced to 0
            raw_values[calc.key] = value
            result.sub_scores[calc.key] = SubScoreResult(
                key=calc.key,
                value=value,
                weight=self.config.weight(calc.key),
                instrument=calc.instrument,
                present=value is not None,
            )

        # 3. Weighted aggregation over present data.
        try:
            overall = self.aggregator.aggregate(raw_values, self.config.weights.weights)
            result.overall_score = round(overall, 1)
            result.risk_level = RiskLevel.from_score(result.overall_score)
        except CalculatorError:
            result.overall_score = None
            result.risk_level = None  # needs-review state; caller should route to manual review

        # 4. Data completeness / confidence.
        completeness = self.aggregator.completeness_pct(raw_values)
        result.completeness_pct = completeness
        result.data_confidence = DataConfidence.from_completeness(completeness)

        # 5. Explanation engine.
        result.top_risk_drivers = self.explanation_engine.top_drivers(raw_values, patient, n=5)

        # 6. Screening gaps (pass-through from patient data, already evaluated
        #    upstream against the active locale schedule).
        result.screening_gaps = [
            {"key": g.key, "category": g.category, "status": g.status}
            for g in getattr(patient, "screening_gaps", []) or []
        ]

        # 7. Interventions + escalation.
        result.recommended_actions = self.intervention_engine.recommend(
            result.risk_level, raw_values, patient
        )
        result.escalation_level = self.escalation_engine.escalation_tier(
            result.risk_level, raw_values, patient, red_flags
        )

        return result

    @staticmethod
    def _completeness(patient: Any) -> float:
        """Rough completeness estimate used only for the red-flag short-circuit
        path (Section 8: 'the engine always emits a confidence indicator')."""
        v = patient.vitals
        fields = [v.respiratory_rate, v.spo2, v.systolic_bp, v.heart_rate, v.temperature]
        present = sum(1 for f in fields if f.is_present)
        return round(100.0 * present / len(fields), 1)
