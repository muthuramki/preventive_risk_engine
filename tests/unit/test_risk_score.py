"""End-to-end pipeline test against the spec's Section 8.2 worked scenario."""

from examples.risk_score_example import build_example_patient
from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine
from preventive_risk_engine.enums.risk_level import RiskLevel


def test_worked_example_no_red_flag_and_valid_score():
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    engine = RiskScoreEngine(config)
    result = engine.run(patient)

    assert result.red_flag is False
    assert result.overall_score is not None
    assert 0 <= result.overall_score <= 100
    assert result.risk_level is not None
    assert len(result.top_risk_drivers) <= 5
    assert result.escalation_level is not None


def test_response_shape_matches_contract():
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    engine = RiskScoreEngine(config)
    result = engine.run(patient)
    response = result.to_api_response()

    for field in ["patient_id", "risk_score", "risk_level", "red_flag", "data_confidence",
                  "sub_scores", "instrument_provenance", "top_risk_drivers",
                  "screening_gaps", "recommended_actions", "escalation_level",
                  "rules_version", "locale", "disclaimer"]:
        assert field in response, f"missing {field}"
