"""Public entry point: RiskScoreEngine.run(patient) -> RiskResult."""

from typing import Any

from preventive_risk_engine.base.base_engine import BaseEngine
from preventive_risk_engine.engines.risk_score.pipeline import RiskScorePipeline
from preventive_risk_engine.models.risk_result import RiskResult


class RiskScoreEngine(BaseEngine):
    name = "risk_score"

    def __init__(self, config: Any):
        super().__init__(config)
        self.pipeline = RiskScorePipeline(config)

    def run(self, patient: Any) -> RiskResult:
        return self.pipeline.run(patient)
