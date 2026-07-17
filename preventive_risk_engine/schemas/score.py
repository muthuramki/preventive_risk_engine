"""Lightweight schema for a single sub-score entry, mirroring
models.risk_result.SubScoreResult for (de)serialization boundaries."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SubScoreSchema:
    key: str
    value: Optional[float]
    weight: float
    instrument: str
