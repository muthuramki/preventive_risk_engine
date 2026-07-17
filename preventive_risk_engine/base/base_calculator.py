"""Abstract base for the eight rules-based sub-score calculators.

Each calculator wraps one validated clinical instrument (NEWS2, Charlson,
LACE, Beers/STOPP-START, PDC, HEDIS, USPSTF/India schedules, SDOH) and
returns a 0-100 internal sub-score, or None if there isn't enough data to
compute it safely (Section 13: 'Safe failure').
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from preventive_risk_engine.exceptions.calculator_exception import CalculatorError
from preventive_risk_engine.config.constants.score_constants import MIN_SUBSCORE, MAX_SUBSCORE


class BaseCalculator(ABC):
    #: short key used in sub_scores dict, e.g. "acute_deterioration"
    key: str = "base"
    #: name of the validated instrument this wraps, e.g. "NEWS2"
    instrument: str = "unspecified"

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    def is_computable(self, patient: Any) -> bool:
        """Return True if there is enough data present to compute this
        sub-score at all. If False, the caller should mark it missing and
        renormalize weights rather than defaulting to 0."""

    @abstractmethod
    def _compute_raw(self, patient: Any) -> float:
        """Compute the raw, possibly >100 or <0, point total before capping."""

    def compute(self, patient: Any) -> Optional[float]:
        if not self.is_computable(patient):
            return None
        try:
            raw = self._compute_raw(patient)
        except Exception as exc:  # noqa: broad-except is intentional here
            raise CalculatorError(
                f"{self.__class__.__name__} failed to compute a sub-score: {exc}"
            ) from exc
        return self._cap(raw)

    @staticmethod
    def _cap(value: float) -> float:
        return max(MIN_SUBSCORE, min(MAX_SUBSCORE, value))

    @staticmethod
    def lookup_band(value: float, bands) -> int:
        """Shared helper: given value and a list of (low, high, points)
        inclusive bands, return the matching points. Raises if no band
        matches (should never happen with well-formed, open-ended bands)."""
        for low, high, points in bands:
            if low <= value <= high:
                return points
        raise CalculatorError(f"No lookup band matched value={value}")
