from .engine_exception import EngineError


class CalculatorError(EngineError):
    """Raised when a sub-score calculator cannot safely produce a value.

    Per Section 13, a calculator error must make that sub-score 'missing'
    (excluded + renormalized), never silently coerced to 0.
    """
