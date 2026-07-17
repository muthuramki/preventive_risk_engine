from preventive_risk_engine.engines.bmi.calculator import calculate_bmi, bmi_category
from preventive_risk_engine.engines.bmi.config import BMIConfig


def test_bmi_calculation():
    assert calculate_bmi(70, 1.75) == 22.9


def test_bmi_category():
    config = BMIConfig()
    assert bmi_category(17.0, config) == "Underweight"
    assert bmi_category(22.0, config) == "Normal"
    assert bmi_category(28.0, config) == "Overweight"
    assert bmi_category(32.0, config) == "Obese"
