"""Integration test: full pipeline run from build_example_patient() through
to a red-flag scenario, ensuring the two paths (normal vs. red-flag) both
behave per Section 8."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from datetime import date

from examples.risk_score_example import build_example_patient
from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine
from preventive_risk_engine.models.patient import DataField


def test_normal_patient_produces_banded_score():
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    result = RiskScoreEngine(config).run(patient)
    assert result.red_flag is False
    assert result.overall_score is not None


def test_critical_spo2_triggers_red_flag_short_circuit():
    patient = build_example_patient()
    patient.vitals.spo2 = DataField(value=85)  # critical hypoxia
    config = load_rules_config(locale=patient.locale)
    result = RiskScoreEngine(config).run(patient)
    assert result.red_flag is True
    assert result.overall_score is None
    assert result.escalation_level.value == "Emergency escalation"
