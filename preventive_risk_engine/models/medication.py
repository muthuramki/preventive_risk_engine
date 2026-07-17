"""Medication and adherence records (Section 7.4 / 7.5)."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class MedicationRecord:
    name: str
    drug_class: Optional[str] = None  # "anticoagulant" | "insulin" | "sulfonylurea" | "opioid" | "sedative" | ...
    is_beers_listed: bool = False
    start_date: Optional[date] = None
    last_changed_date: Optional[date] = None
    active: bool = True


@dataclass
class AdherenceRecord:
    """Proportion of Days Covered (PDC) inputs (Section 0.2 / 7.5)."""
    days_covered: int = 0
    days_in_window: int = 1

    @property
    def pdc(self) -> float:
        if self.days_in_window <= 0:
            return 0.0
        return round(100.0 * self.days_covered / self.days_in_window, 1)


@dataclass
class MedicationProfile:
    medications: list = field(default_factory=list)          # list[MedicationRecord]
    adherence: Optional[AdherenceRecord] = None
    missed_appointments_6m: int = 0
    missed_or_declined_critical_tasks: int = 0
    has_known_interaction: bool = False

    @property
    def active_count(self) -> int:
        return sum(1 for m in self.medications if m.active)

    @property
    def beers_listed_active(self) -> list:
        return [m for m in self.medications if m.active and m.is_beers_listed]

    def has_recent_change(self, as_of: date, within_days: int = 30) -> bool:
        return any(
            m.last_changed_date is not None
            and (as_of - m.last_changed_date).days <= within_days
            for m in self.medications
        )
