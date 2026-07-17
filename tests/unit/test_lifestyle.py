from preventive_risk_engine.engines.risk_score.calculators.lifestyle_calculator import LifestyleSocialCalculator
from preventive_risk_engine.models.lifestyle import LifestyleProfile


class DummyPatient:
    def __init__(self, lifestyle):
        self.lifestyle = lifestyle


def test_unknown_fields_do_not_crash(us_config):
    calc = LifestyleSocialCalculator(us_config)
    p = DummyPatient(LifestyleProfile())  # everything unknown/None
    assert calc.compute(p) == 0


def test_social_barriers_capped(us_config):
    calc = LifestyleSocialCalculator(us_config)
    p = DummyPatient(LifestyleProfile(
        food_insecurity=True, transport_barrier=True,
        financial_barrier=True, social_isolation=True,
    ))
    assert calc.compute(p) <= 40
