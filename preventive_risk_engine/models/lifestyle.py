"""SDOH / lifestyle profile (Section 0.2 / 7.8). These points route to
support resources and must NEVER lower a patient's care priority."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LifestyleProfile:
    current_smoker: Optional[bool] = None
    heavy_alcohol_use: Optional[bool] = None
    sedentary: Optional[bool] = None
    poor_diet: Optional[bool] = None
    poor_sleep: Optional[bool] = None
    high_stress: Optional[bool] = None
    social_isolation: Optional[bool] = None
    transport_barrier: Optional[bool] = None
    financial_barrier: Optional[bool] = None
    food_insecurity: Optional[bool] = None

    def known_fields(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items() if v is not None
        }
