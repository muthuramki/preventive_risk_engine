"""Compliance / adherence, PDC-derived (Section 7.5)."""

from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator


class AdherenceCalculator(BaseCalculator):
    key = "compliance_adherence"
    instrument = "Proportion of Days Covered (PDC)"

    def is_computable(self, patient: Any) -> bool:
        adherence = getattr(patient, "adherence", None)
        return adherence is not None

    def _compute_raw(self, patient: Any) -> float:
        adherence = patient.adherence  # AdherenceRecord-like, has .pdc
        total = 0.0

        pdc = adherence.pdc
        if pdc < 50:
            total += 35
        elif pdc < 80:
            total += 20

        missed_appts = getattr(patient, "missed_appointments_6m", 0) or 0
        if missed_appts >= 2:
            total += 20

        missed_tasks = getattr(patient, "missed_or_declined_critical_tasks", 0) or 0
        if missed_tasks > 0:
            total += 15

        return total
