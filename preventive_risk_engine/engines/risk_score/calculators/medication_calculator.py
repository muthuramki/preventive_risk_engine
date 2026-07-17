"""Medication risk, Beers/STOPP-START + polypharmacy derived (Section 7.4)."""

from datetime import date
from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator

HIGH_RISK_CLASSES = {"anticoagulant", "insulin", "sulfonylurea", "opioid", "sedative"}


class MedicationRiskCalculator(BaseCalculator):
    key = "medication"
    instrument = "Beers Criteria / STOPP-START + polypharmacy"

    def is_computable(self, patient: Any) -> bool:
        return patient.medications is not None

    def _compute_raw(self, patient: Any) -> float:
        meds = [m for m in patient.medications if getattr(m, "active", True)]
        n = len(meds)
        total = 0.0

        # Polypharmacy (Section 7.4).
        if n >= 10:
            total += 30
        elif n >= 5:
            total += 15

        # Beers-listed / high-risk medication hits, capped cumulative at 40
        # (i.e. up to 4 distinct hits) to avoid runaway scores.
        high_risk_hits = sum(
            1 for m in meds
            if getattr(m, "is_beers_listed", False) or getattr(m, "drug_class", None) in HIGH_RISK_CLASSES
        )
        total += min(40, high_risk_hits * 10)

        # Recent significant change (<30 days).
        as_of = date.today()
        if any(
            getattr(m, "last_changed_date", None) is not None
            and (as_of - m.last_changed_date).days < 30
            for m in meds
        ):
            total += 10

        # Known interaction flag (patient-level or profile-level).
        if getattr(patient, "has_known_interaction", False):
            total += 15

        return total
