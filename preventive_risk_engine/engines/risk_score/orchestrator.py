"""Thin orchestration layer: loads config for the patient's locale and runs
the engine. This is what a service/API layer should call."""

from typing import Any

from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine
from preventive_risk_engine.models.risk_result import RiskResult


def score_patient(patient: Any) -> RiskResult:
    config = load_rules_config(locale=patient.locale)
    engine = RiskScoreEngine(config)
    return engine.run(patient)
