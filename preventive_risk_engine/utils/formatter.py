"""Formatting helpers for human-readable output (dashboards, logs)."""

from typing import Optional


def format_score(value: Optional[float]) -> str:
    return "N/A" if value is None else f"{value:.1f}"


def format_band(band: Optional[str]) -> str:
    return band or "Needs Review"
