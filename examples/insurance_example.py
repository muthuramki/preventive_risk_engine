"""Illustrative only -- not a validated actuarial model."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from examples.risk_score_example import build_example_patient
from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine
from preventive_risk_engine.engines.insurance.engine import InsuranceEngine

if __name__ == "__main__":
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    result = RiskScoreEngine(config).run(patient)
    print(InsuranceEngine().run(result))
