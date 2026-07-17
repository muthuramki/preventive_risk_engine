"""Escalation priority tiers (Section 9 / Table 8)."""

from enum import Enum


class EscalationTier(str, Enum):
    ROUTINE_FOLLOW_UP = "Routine follow-up"
    NURSE_REVIEW = "Nurse review"
    PHYSICIAN_REVIEW = "Physician review"
    URGENT_CARE = "Urgent care recommendation"
    EMERGENCY_ESCALATION = "Emergency escalation"


class AVPU(str, Enum):
    """Consciousness scale used by NEWS2. Anything other than ALERT scores 3 points."""
    ALERT = "A"
    VOICE = "V"
    PAIN = "P"
    UNRESPONSIVE = "U"
