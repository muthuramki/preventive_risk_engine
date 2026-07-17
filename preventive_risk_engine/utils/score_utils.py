"""Small numeric helpers shared by calculators."""

from typing import Iterable


def cap(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def sum_capped(points: Iterable[float], cap_value: float) -> float:
    return min(cap_value, sum(points))
