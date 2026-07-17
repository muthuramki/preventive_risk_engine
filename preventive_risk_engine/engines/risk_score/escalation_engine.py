"""Five-tier escalation ladder (Section 9 / Table 8).

These are recommendations to humans, not automated dispatch in the MVP.
Every escalation and every clinician override of one must be logged
(enforced by the audit layer, not here)."""

from typing import Any, Dict, List, Optional

from preventive_risk_engine.base.base_escalation import BaseEscalation
from preventive_risk_engine.enums.risk_level import RiskLevel
from preventive_risk_engine.enums.priority import EscalationTier


class EscalationEngine(BaseEscalation):
    def escalation_tier(
        self,
        risk_level: Optional[RiskLevel],
        sub_scores: Dict[str, Any],
        patient: Any,
        red_flags: List,
    ) -> EscalationTier:
        # Any red-flag override -> bypass scoring, direct to emergency pathway.
        if red_flags:
            return EscalationTier.EMERGENCY_ESCALATION

        if risk_level is None:
            return EscalationTier.PHYSICIAN_REVIEW  # safe-failure default: needs review

        if risk_level == RiskLevel.CRITICAL:
            return EscalationTier.URGENT_CARE

        if risk_level == RiskLevel.HIGH:
            return EscalationTier.PHYSICIAN_REVIEW

        if risk_level in (RiskLevel.MILD, RiskLevel.MODERATE):
            adherence = sub_scores.get("compliance_adherence")
            care_gap = sub_scores.get("care_gap")
            rising_trend = getattr(patient.vitals, "rr_trend_rising", False) or \
                getattr(patient.vitals, "spo2_trend_falling", False)
            if rising_trend or (adherence is not None and adherence >= 40) or \
                    (care_gap is not None and care_gap >= 40):
                return EscalationTier.NURSE_REVIEW
            return EscalationTier.ROUTINE_FOLLOW_UP if risk_level == RiskLevel.MILD else EscalationTier.NURSE_REVIEW

        return EscalationTier.ROUTINE_FOLLOW_UP
