"""Abstract base for input validators."""

from abc import ABC, abstractmethod
from typing import Any, List


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, data: Any) -> List[str]:
        """Return a list of human-readable validation error strings.
        Empty list means valid."""
