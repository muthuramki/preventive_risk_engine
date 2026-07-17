from .engine_exception import EngineError


class ValidationError(EngineError):
    """Raised when input data fails structural or clinical validation."""
