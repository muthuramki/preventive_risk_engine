from dataclasses import dataclass


@dataclass
class PredictionConfig:
    """Post-MVP ML roadmap scaffold (Section 18). No trained model ships
    with the MVP; this is a placeholder interface only."""
    model_name: str = "not_yet_trained"
