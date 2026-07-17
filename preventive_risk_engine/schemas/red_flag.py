"""Schema for red-flag override payload entries."""

from dataclasses import dataclass


@dataclass
class RedFlagSchema:
    code: str
    description: str
    source: str
