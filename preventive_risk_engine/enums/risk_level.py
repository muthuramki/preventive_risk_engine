"""
Risk level bands (Section 4 of the spec).

Bands are advisory only — a red-flag override can escalate a low-scoring
patient straight to emergency care, and a clinician can override any band
with a logged reason.
"""

from enum import Enum


class RiskLevel(str, Enum):
    LOW = "Low"
    MILD = "Mild"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

    @classmethod
    def from_score(cls, score: float) -> "RiskLevel":
        """Map an overall 0-100 score onto a band (Section 4 / Table 3)."""
        if score < 0 or score > 100:
            raise ValueError(f"Overall score must be within 0-100, got {score}")
        if score <= 20:
            return cls.LOW
        if score <= 40:
            return cls.MILD
        if score <= 60:
            return cls.MODERATE
        if score <= 80:
            return cls.HIGH
        return cls.CRITICAL


class DataConfidence(str, Enum):
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"
    INSUFFICIENT = "Insufficient"

    @classmethod
    def from_completeness(cls, pct: float) -> "DataConfidence":
        """Map completeness percentage (0-100) onto a confidence level (Table 12)."""
        if pct >= 90:
            return cls.HIGH
        if pct >= 70:
            return cls.MODERATE
        if pct >= 50:
            return cls.LOW
        return cls.INSUFFICIENT
