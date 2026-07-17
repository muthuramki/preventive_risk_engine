from typing import Any

from preventive_risk_engine.base.base_engine import BaseEngine
from preventive_risk_engine.engines.insurance.calculator import insurance_band
from preventive_risk_engine.engines.insurance.config import InsuranceConfig


class InsuranceEngine(BaseEngine):
    name = "insurance"

    def __init__(self, config: Any = None):
        super().__init__(config or InsuranceConfig())

    def run(self, risk_result: Any) -> dict:
        return {"insurance_band": insurance_band(risk_result.overall_score, self.config)}
