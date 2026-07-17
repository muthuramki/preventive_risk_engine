from dataclasses import dataclass


@dataclass
class InsuranceConfig:
    """Placeholder config for a future insurance-risk-banding engine
    (not part of the MVP clinical spec; kept as a scaffold slot)."""
    high_risk_score_threshold: int = 61
