"""Schema for the top-5 driver explanation payload."""

from dataclasses import dataclass
from typing import List


@dataclass
class ExplanationSchema:
    top_risk_drivers: List[str]
