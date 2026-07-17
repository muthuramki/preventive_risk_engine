from .engine_exception import EngineError


class ConfigurationError(EngineError):
    """Raised for malformed or missing clinical configuration (weights,
    thresholds, red-flag rules, locale packs)."""
