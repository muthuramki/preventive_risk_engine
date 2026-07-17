"""Abstract base for role-based intervention recommendation engines."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseIntervention(ABC):
    @abstractmethod
    def recommend(self, risk_level: Any, sub_scores: Dict[str, Any], patient: Any) -> Dict[str, List[str]]:
        """Return a dict of role -> list of recommended actions."""
