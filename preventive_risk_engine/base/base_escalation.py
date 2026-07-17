"""Abstract base for the five-tier escalation engine."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseEscalation(ABC):
    @abstractmethod
    def escalation_tier(self, risk_level: Any, sub_scores: Dict[str, Any], patient: Any, red_flags: list) -> Any:
        """Return the EscalationTier for this patient/run."""
