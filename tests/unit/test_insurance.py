from preventive_risk_engine.engines.insurance.calculator import insurance_band
from preventive_risk_engine.engines.insurance.config import InsuranceConfig


def test_insurance_band_high():
    config = InsuranceConfig()
    assert insurance_band(75, config) == "High Utilization Risk"


def test_insurance_band_standard():
    config = InsuranceConfig()
    assert insurance_band(30, config) == "Standard"


def test_insurance_band_needs_review():
    config = InsuranceConfig()
    assert insurance_band(None, config) == "Needs Review"
