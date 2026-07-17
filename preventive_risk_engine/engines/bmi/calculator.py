"""BMI = weight(kg) / height(m)^2 (glossary, Table 1)."""


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("height_m must be > 0")
    return round(weight_kg / (height_m ** 2), 1)


def bmi_category(bmi: float, config) -> str:
    if bmi < config.underweight_max:
        return "Underweight"
    if bmi < config.normal_max:
        return "Normal"
    if bmi < config.overweight_max:
        return "Overweight"
    return "Obese"
