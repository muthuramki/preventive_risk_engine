"""Abstract base for score aggregators (weighted-mean renormalization)."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAggregator(ABC):
    @abstractmethod
    def aggregate(self, sub_scores: Dict[str, Any], weights: Dict[str, float]) -> float:
        """Combine sub-scores into a single 0-100 overall score."""
