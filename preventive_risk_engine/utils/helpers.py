"""Miscellaneous small helpers used across calculators/engines."""

from typing import Any, Optional


def safe_get(obj: Any, attr: str, default: Any = None) -> Any:
    return getattr(obj, attr, default) if obj is not None else default


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
