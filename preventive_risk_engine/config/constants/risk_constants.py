"""
Published NEWS2 point tables (Royal College of Physicians NEWS2, 2017).

These are lookup-table thresholds, NOT invented math. They are treated as
clinician-confirmed configuration per the spec (Section 0.2 / 7.1) and are
also mirrored in resources/scoring_config.yaml so they can be re-tuned
without a code change.

Each table is a list of (low, high, points) bands, inclusive on both ends.
Use math.inf / -math.inf for open-ended bands.
"""

import math

# ---------------------------------------------------------------------------
# Respiratory Rate (breaths/min)
# ---------------------------------------------------------------------------
RESPIRATORY_RATE_BANDS = [
    (-math.inf, 8, 3),
    (9, 11, 1),
    (12, 20, 0),
    (21, 24, 2),
    (25, math.inf, 3),
]

# ---------------------------------------------------------------------------
# SpO2 (%) — standard NEWS2 scale (Scale 1, no hypercapnic-respiratory-failure
# adjustment). Scale 2 (for COPD/target-88-92% patients) can be added as a
# separate configured table when clinically confirmed.
# ---------------------------------------------------------------------------
SPO2_BANDS = [
    (-math.inf, 91, 3),
    (92, 93, 2),
    (94, 95, 1),
    (96, math.inf, 0),
]

# ---------------------------------------------------------------------------
# Systolic Blood Pressure (mmHg)
# ---------------------------------------------------------------------------
SYSTOLIC_BP_BANDS = [
    (-math.inf, 90, 3),
    (91, 100, 2),
    (101, 110, 1),
    (111, 219, 0),
    (220, math.inf, 3),
]

# ---------------------------------------------------------------------------
# Heart Rate (bpm)
# ---------------------------------------------------------------------------
HEART_RATE_BANDS = [
    (-math.inf, 40, 3),
    (41, 50, 1),
    (51, 90, 0),
    (91, 110, 1),
    (111, 130, 2),
    (131, math.inf, 3),
]

# ---------------------------------------------------------------------------
# Temperature (°C)
# ---------------------------------------------------------------------------
TEMPERATURE_BANDS = [
    (-math.inf, 35.0, 3),
    (35.1, 36.0, 1),
    (36.1, 38.0, 0),
    (38.1, 39.0, 1),
    (39.1, math.inf, 2),
]

# ---------------------------------------------------------------------------
# Supplemental oxygen — NEWS2 adds 2 points whenever the patient is on any
# supplemental O2, regardless of the SpO2 reading itself.
# ---------------------------------------------------------------------------
SUPPLEMENTAL_OXYGEN_POINTS = 2

# ---------------------------------------------------------------------------
# AVPU consciousness — Alert scores 0; anything else (Voice/Pain/Unresponsive,
# i.e. "new confusion") scores 3.
# ---------------------------------------------------------------------------
AVPU_ALERT_POINTS = 0
AVPU_NOT_ALERT_POINTS = 3

# ---------------------------------------------------------------------------
# NEWS2 aggregate -> qualitative band (Section 7.1).
# Aggregate is the sum of the seven parameter points above (typically 0-20+).
# A single-parameter score of 3 in any one vital ("red score") also counts as
# high risk even if the total is below 5, per standard NEWS2 escalation
# protocol -- handled in the calculator, not here.
# ---------------------------------------------------------------------------
NEWS2_BAND_THRESHOLDS = [
    (0, 2, "low"),
    (3, 4, "moderate"),
    (5, 6, "high"),
    (7, math.inf, "critical"),
]

# NEWS2 total at/above this value is a mandatory red-flag override (Section 7.9)
NEWS2_RED_FLAG_THRESHOLD = 7
