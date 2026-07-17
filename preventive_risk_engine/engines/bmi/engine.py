from typing import Any

from preventive_risk_engine.base.base_engine import BaseEngine
from preventive_risk_engine.engines.bmi.calculator import calculate_bmi, bmi_category
from preventive_risk_engine.engines.bmi.config import BMIConfig


class BMIEngine(BaseEngine):
    name = "bmi"

    def __init__(self, config: Any = None):
        super().__init__(config or BMIConfig())

    def run(self, weight_kg: float, height_m: float) -> dict:
        bmi = calculate_bmi(weight_kg, height_m)
        return {"bmi": bmi, "category": bmi_category(bmi, self.config)}
