from typing import Any

from preventive_risk_engine.base.base_engine import BaseEngine
from preventive_risk_engine.engines.prediction.predictor import predict
from preventive_risk_engine.engines.prediction.config import PredictionConfig


class PredictionEngine(BaseEngine):
    name = "prediction"

    def __init__(self, config: Any = None):
        super().__init__(config or PredictionConfig())

    def run(self, features: dict) -> dict:
        return {"predicted_risk": predict(features, self.config), "model": self.config.model_name}
