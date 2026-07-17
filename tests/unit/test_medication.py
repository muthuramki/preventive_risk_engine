from preventive_risk_engine.engines.risk_score.calculators.medication_calculator import MedicationRiskCalculator
from preventive_risk_engine.models.medication import MedicationRecord


class DummyPatient:
    def __init__(self, meds):
        self.medications = meds
        self.has_known_interaction = False


def test_polypharmacy_threshold(us_config):
    calc = MedicationRiskCalculator(us_config)
    meds = [MedicationRecord(name=f"Drug{i}") for i in range(10)]
    p = DummyPatient(meds)
    assert calc.compute(p) >= 30
