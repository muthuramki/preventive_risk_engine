from enum import Enum


class ChronicCondition(str, Enum):
    """Qualifying chronic conditions for the Charlson-derived sub-score (Section 7.2)."""
    DIABETES = "diabetes"
    DIABETES_WITH_COMPLICATIONS = "diabetes_with_complications"
    HYPERTENSION = "hypertension"
    HEART_FAILURE = "heart_failure"
    CKD_STAGE_1_3 = "ckd_stage_1_3"
    CKD_STAGE_4 = "ckd_stage_4"
    CKD_STAGE_5 = "ckd_stage_5"  # end-stage renal disease
    COPD = "copd"
    CANCER_ACTIVE = "cancer_active"
    CANCER_REMISSION = "cancer_remission"
    PRIOR_STROKE_TIA = "prior_stroke_tia"
    MENTAL_HEALTH = "mental_health_condition"


class IntervnetionRole(str, Enum):
    """Kept intentionally distinct from typos in the folder skeleton; see intervention_type.py"""
    pass
