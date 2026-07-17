"""Runtime-editable weights wrapper (Section 6)."""

from dataclasses import dataclass, field
from typing import Dict
from preventive_risk_engine.config.constants.score_constants import DEFAULT_WEIGHTS



@dataclass
class WeightConfig:
    weights: Dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))

    def __getitem__(self, key: str) -> float:
        return self.weights[key]

    def total(self) -> float:
        return sum(self.weights.values())

    def renormalized(self, present_keys) -> Dict[str, float]:
        """Weights for only the sub-scores actually present, per Section 8:
        overall = SUM(subscore_i * weight_i) / SUM(weight_i present)."""
        return {k: self.weights[k] for k in present_keys if k in self.weights}
