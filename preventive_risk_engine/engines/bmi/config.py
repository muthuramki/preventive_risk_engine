from dataclasses import dataclass


@dataclass
class BMIConfig:
    underweight_max: float = 18.5
    normal_max: float = 25.0
    overweight_max: float = 30.0
