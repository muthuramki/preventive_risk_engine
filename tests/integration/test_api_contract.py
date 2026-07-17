"""Confirms RiskResult.to_api_response() matches Section 11's contract shape."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from examples.risk_score_example import build_example_patient
from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine
from preventive_risk_engine.schemas.response import validate_response_shape


def test_api_response_has_all_required_fields():
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    result = RiskScoreEngine(config).run(patient)
    response = result.to_api_response()
    missing = validate_response_shape(response)
    assert missing == []
