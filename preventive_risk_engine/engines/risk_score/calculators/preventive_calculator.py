"""Preventive care: overdue age/sex screenings & immunizations (Section 7.7,
Appendix A). Schedule source is the active locale pack (US: USPSTF/ADA/ACIP;
India: NP-NCD)."""

from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator

POINTS_PER_OPEN_GAP = 10
PREVENTIVE_CAP = 50


class PreventiveCareCalculator(BaseCalculator):
    key = "preventive_care"
    instrument = "USPSTF / India (NP-NCD) screening schedules"

    def is_computable(self, patient: Any) -> bool:
        return getattr(patient, "screening_gaps", None) is not None

    def _compute_raw(self, patient: Any) -> float:
        gaps = [
            g for g in patient.screening_gaps
            if getattr(g, "category", None) == "preventive_care" and getattr(g, "status", None) == "overdue"
        ]
        return min(PREVENTIVE_CAP, len(gaps) * POINTS_PER_OPEN_GAP)
