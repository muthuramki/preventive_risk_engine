"""Lifestyle / social (SDOH) sub-score (Section 7.8).

EQUITY GUARDRAIL (Table 6): these points exist to *route the patient to
support resources*. They must never be used to lower a patient's priority,
eligibility, or care -- only ever to raise attention/routing to a
care-coordinator. Enforce this at the intervention layer, not here.
"""

from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator

SOCIAL_BARRIER_POINTS = 10
SOCIAL_BARRIER_CAP = 40


class LifestyleSocialCalculator(BaseCalculator):
    key = "lifestyle_social"
    instrument = "SDOH screening"

    def is_computable(self, patient: Any) -> bool:
        return getattr(patient, "lifestyle", None) is not None

    def _compute_raw(self, patient: Any) -> float:
        lc = patient.lifestyle
        total = 0.0

        def flag(name: str) -> bool:
            # Optional[bool] fields default to None (unknown), which must be
            # treated as falsy here, not crash arithmetic downstream.
            return bool(getattr(lc, name, None))

        if flag("current_smoker"):
            total += 15
        if flag("heavy_alcohol_use"):
            total += 10

        sedentary_cluster = all([flag("sedentary"), flag("poor_diet"), flag("poor_sleep")])
        if sedentary_cluster:
            total += 10

        social_barriers = [
            flag("food_insecurity"),
            flag("transport_barrier"),
            flag("financial_barrier"),
            flag("social_isolation"),
        ]
        total += min(SOCIAL_BARRIER_CAP, sum(social_barriers) * SOCIAL_BARRIER_POINTS)

        return total
