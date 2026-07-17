from preventive_risk_engine.engines.risk_score.calculators.chronic_calculator import ChronicBurdenCalculator
from preventive_risk_engine.models.admission import ConditionRecord
from preventive_risk_engine.enums.disease_type import ChronicCondition


class DummyPatient:
    def __init__(self, conditions):
        self.conditions = conditions


def test_multimorbidity_bump(us_config):
    calc = ChronicBurdenCalculator(us_config)
    conditions = [
        ConditionRecord(condition=ChronicCondition.DIABETES),
        ConditionRecord(condition=ChronicCondition.HYPERTENSION),
        ConditionRecord(condition=ChronicCondition.HEART_FAILURE),
    ]
    p = DummyPatient(conditions)
    score = calc.compute(p)
    assert score is not None and score > 0


def test_active_cancer_high_contribution(us_config):
    calc = ChronicBurdenCalculator(us_config)
    p = DummyPatient([ConditionRecord(condition=ChronicCondition.CANCER_ACTIVE)])
    assert calc.compute(p) >= 80
