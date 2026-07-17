"""Abstract base for the explanation engine."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseExplainer(ABC):
    @abstractmethod
    def top_drivers(self, sub_scores: Dict[str, Any], patient: Any, n: int = 5) -> List[str]:
        """Return up to n plain-language driver strings, highest impact first."""
