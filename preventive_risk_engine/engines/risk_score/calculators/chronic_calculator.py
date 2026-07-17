"""Chronic disease burden, Charlson-derived (Section 7.2)."""

from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator
from preventive_risk_engine.enums.disease_type import ChronicCondition

# Simplified Charlson-style weights (illustrative starting values --
# clinician-tunable per the spec). Real deployments should load the full
# published Charlson weight table from config.
CONDITION_WEIGHTS = {
    ChronicCondition.DIABETES: 10,
    ChronicCondition.DIABETES_WITH_COMPLICATIONS: 18,
    ChronicCondition.HYPERTENSION: 5,
    ChronicCondition.HEART_FAILURE: 20,
    ChronicCondition.CKD_STAGE_1_3: 8,
    ChronicCondition.CKD_STAGE_4: 15,
    ChronicCondition.CKD_STAGE_5: 30,
    ChronicCondition.COPD: 12,
    ChronicCondition.CANCER_ACTIVE: 30,
    ChronicCondition.CANCER_REMISSION: 10,
    ChronicCondition.PRIOR_STROKE_TIA: 15,
    ChronicCondition.MENTAL_HEALTH: 8,
}

HIGH_CONTRIBUTION_CONDITIONS = {
    ChronicCondition.CANCER_ACTIVE,
    ChronicCondition.CKD_STAGE_5,
}


class ChronicBurdenCalculator(BaseCalculator):
    key = "chronic_disease_burden"
    instrument = "Charlson Comorbidity Index"

    def is_computable(self, patient: Any) -> bool:
        return patient.conditions is not None

    def _compute_raw(self, patient: Any) -> float:
        active = [c for c in patient.conditions if getattr(c, "active", True)]
        n_active = len(active)

        total = 0.0
        for c in active:
            total += CONDITION_WEIGHTS.get(c.condition, 5)

        # Multimorbidity super-additive bumps (Section 7.2).
        if n_active >= 5:
            total += 30
        elif n_active >= 3:
            total += 15

        # Active cancer or end-stage organ disease -> high contribution.
        if any(c.condition in HIGH_CONTRIBUTION_CONDITIONS for c in active):
            total = max(total, 80)
            if any(
                c.condition == ChronicCondition.HEART_FAILURE and c.severity == "decompensated"
                for c in active
            ):
                total = max(total, 85)

        return total
