"""
RulesConfig: the single object threaded through every calculator/engine.

Everything clinician-tunable (weights, red-flag thresholds, freshness
windows, screening schedules) lives here, sourced from
resources/scoring_config.yaml + resources/locale_*.yaml, so that changing a
threshold never requires a code change (Section 16 / NFR "Configurability").
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from preventive_risk_engine.config.weights import WeightConfig
from preventive_risk_engine.enums.locale import Locale


@dataclass
class LocalePack:
    locale: Locale
    units: Dict[str, str] = field(default_factory=dict)
    reference_ranges: Dict[str, Any] = field(default_factory=dict)
    guideline_targets: Dict[str, Any] = field(default_factory=dict)
    schedule: list = field(default_factory=list)  # list of screening-schedule rows


@dataclass
class RedFlagConfig:
    """Section 7.9 — thresholds for hard overrides outside the weighted sum."""
    news2_critical_threshold: int = 7
    spo2_critical_threshold: int = 91
    single_parameter_extreme_points: int = 3  # any one NEWS2 vital scoring 3 = red flag
    acute_symptom_flags: tuple = ("chest_pain", "suspected_stroke", "suicidal_ideation")


@dataclass
class RulesConfig:
    version: str = "rules_v2.0"
    weights: WeightConfig = field(default_factory=WeightConfig)
    red_flags: RedFlagConfig = field(default_factory=RedFlagConfig)
    locale_pack: Optional[LocalePack] = None

    # freshness windows, keyed by field name -> days
    freshness_windows_days: Dict[str, int] = field(default_factory=lambda: {
        "hba1c": 425,       # ~14 months
        "eye_exam": 730,
        "foot_exam": 365,
    })

    def weight(self, key: str) -> float:
        return self.weights[key]
