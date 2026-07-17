"""Condition and utilization (admission/ED/ICU) records (Section 7.2 / 7.3)."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from preventive_risk_engine.enums.disease_type import ChronicCondition


@dataclass
class ConditionRecord:
    condition: ChronicCondition
    diagnosis_date: Optional[date] = None
    active: bool = True
    severity: Optional[str] = None  # e.g. "stage_5", "decompensated"


@dataclass
class AdmissionRecord:
    admission_date: date
    discharge_date: Optional[date] = None
    length_of_stay_days: Optional[int] = None
    was_icu: bool = False
    was_30_day_readmission: bool = False
    acuity_level: Optional[str] = None  # e.g. "emergency", "elective"


@dataclass
class EDVisitRecord:
    visit_date: date


@dataclass
class UtilizationHistory:
    """Recency-weighted utilization inputs for the LACE-derived sub-score."""
    admissions: list = field(default_factory=list)   # list[AdmissionRecord]
    ed_visits: list = field(default_factory=list)     # list[EDVisitRecord]

    def admissions_within(self, days: int, as_of: date) -> int:
        return sum(
            1 for a in self.admissions
            if (as_of - a.admission_date).days <= days
        )

    def ed_visits_within(self, days: int, as_of: date) -> int:
        return sum(
            1 for v in self.ed_visits
            if (as_of - v.visit_date).days <= days
        )

    def icu_within(self, days: int, as_of: date) -> bool:
        return any(
            a.was_icu and (as_of - a.admission_date).days <= days
            for a in self.admissions
        )

    def any_30_day_readmission(self) -> bool:
        return any(a.was_30_day_readmission for a in self.admissions)
