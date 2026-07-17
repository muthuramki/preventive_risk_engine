"""Abstract base for the top-level engines (risk_score, bmi, insurance,
prediction)."""

from abc import ABC, abstractmethod
from typing import Any


class BaseEngine(ABC):
    name: str = "base_engine"

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute the engine and return its result object."""
