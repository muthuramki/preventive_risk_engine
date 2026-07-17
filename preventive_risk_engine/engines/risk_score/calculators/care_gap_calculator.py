"""HEDIS-style care gaps (Section 7.6). Diabetic HbA1c/eye/foot exams and
other guideline-recommended actions that are overdue."""

from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator

POINTS_PER_OPEN_GAP = 10
UNCONTROLLED_METRIC_OVERDUE_POINTS = 15
GAP_CAP = 60


class CareGapCalculator(BaseCalculator):
    key = "care_gap"
    instrument = "HEDIS-style care-gap rules"

    def is_computable(self, patient: Any) -> bool:
        return getattr(patient, "screening_gaps", None) is not None

    def _compute_raw(self, patient: Any) -> float:
        gaps = [
            g for g in patient.screening_gaps
            if getattr(g, "category", None) == "care_gap" and getattr(g, "status", None) == "overdue"
        ]
        total = min(GAP_CAP, len(gaps) * POINTS_PER_OPEN_GAP)

        if getattr(patient, "has_uncontrolled_metric_overdue_followup", False):
            total += UNCONTROLLED_METRIC_OVERDUE_POINTS

        return total
