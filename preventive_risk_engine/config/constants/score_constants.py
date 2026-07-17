"""Default sub-score weights (Section 6 / Table 5). Weights sum to 100.

These are an *initial expert prior* per the spec and must be re-tuned
against local outcome data during clinical validation. They are exposed
here as code defaults but the real, editable source of truth at runtime is
resources/scoring_config.yaml (loaded by config/loader.py).
"""

DEFAULT_WEIGHTS = {
    "acute_deterioration": 20,
    "chronic_disease_burden": 18,
    "hospital_readmission": 15,
    "medication": 12,
    "compliance_adherence": 10,
    "lifestyle_social": 10,
    "care_gap": 8,
    "preventive_care": 7,
}

assert sum(DEFAULT_WEIGHTS.values()) == 100, "Sub-score weights must sum to 100"

# Risk band cut points (Section 4 / Table 3), inclusive upper bounds.
RISK_BANDS = [
    (0, 20, "Low"),
    (21, 40, "Mild"),
    (41, 60, "Moderate"),
    (61, 80, "High"),
    (81, 100, "Critical"),
]

# Data completeness -> confidence (Table 12)
CONFIDENCE_BANDS = [
    (90, 100, "High"),
    (70, 89, "Moderate"),
    (50, 69, "Low"),
    (0, 49, "Insufficient"),
]

MAX_SUBSCORE = 100
MIN_SUBSCORE = 0
