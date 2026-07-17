"""Loads scoring_config.yaml + the active locale_*.yaml into a RulesConfig."""

import os
from typing import Optional

import yaml

from preventive_risk_engine.config.settings import RulesConfig, LocalePack, RedFlagConfig
from preventive_risk_engine.config.weights import WeightConfig
from preventive_risk_engine.enums.locale import Locale
from preventive_risk_engine.exceptions.configuration_exception import ConfigurationError

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")


def _load_yaml(filename: str) -> dict:
    path = os.path.join(RESOURCES_DIR, filename)
    if not os.path.exists(path):
        raise ConfigurationError(f"Missing configuration file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_rules_config(locale: Locale = Locale.US) -> RulesConfig:
    scoring = _load_yaml("scoring_config.yaml")

    locale_file = "locale_us.yaml" if locale == Locale.US else "locale_india.yaml"
    locale_data = _load_yaml(locale_file)

    weights = WeightConfig(weights=scoring.get("weights", {}))
    red_flags = RedFlagConfig(**scoring.get("red_flags", {}))

    locale_pack = LocalePack(
        locale=locale,
        units=locale_data.get("units", {}),
        reference_ranges=locale_data.get("reference_ranges", {}),
        guideline_targets=locale_data.get("guideline_targets", {}),
        schedule=locale_data.get("screening_schedule", []),
    )

    return RulesConfig(
        version=scoring.get("version", "rules_v2.0"),
        weights=weights,
        red_flags=red_flags,
        locale_pack=locale_pack,
    )
