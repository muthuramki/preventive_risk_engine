"""Placeholder predictor interface for the post-MVP ML roadmap (Section 18).
Intentionally returns None -- wire in a real model (logistic regression /
gradient-boosted trees / Cox) only after shadow-mode validation."""

from typing import Any, Optional


def predict(features: dict, config: Any) -> Optional[float]:
    return None
