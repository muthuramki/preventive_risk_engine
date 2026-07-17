"""Hospital readmission / utilization, LACE-derived (Section 7.3)."""

from datetime import date
from typing import Any

from preventive_risk_engine.base.base_calculator import BaseCalculator


class ReadmissionCalculator(BaseCalculator):
    key = "hospital_readmission"
    instrument = "LACE index"

    def is_computable(self, patient: Any) -> bool:
        return patient.admissions is not None  # empty list is a valid "no utilization" state

    def _compute_raw(self, patient: Any) -> float:
        as_of = date.today()
        util = _to_utilization_history(patient)

        total = 0.0

        admissions_6m = util.admissions_within(180, as_of)
        admissions_12m = util.admissions_within(365, as_of)
        if admissions_6m >= 2:
            total += 25
        if admissions_12m >= 3:
            total += 35

        if util.any_30_day_readmission():
            total += 30

        ed_6m = util.ed_visits_within(180, as_of)
        if ed_6m >= 2:
            total += 20

        if util.icu_within(365, as_of):
            total += 20

        # Recency weighting: events in the last 3 months count more.
        recent_admissions = util.admissions_within(90, as_of)
        if recent_admissions > 0:
            total += 10 * recent_admissions

        return total


def _to_utilization_history(patient: Any):
    """Adapts patient.admissions (list[AdmissionRecord]) into a
    UtilizationHistory-like object with the helper methods the calculator
    needs, without forcing every caller to pre-build one."""
    from preventive_risk_engine.models.admission import UtilizationHistory, EDVisitRecord

    history = UtilizationHistory(admissions=list(patient.admissions))
    # ED visits may be tracked separately on the patient object; fall back
    # to an empty list if not present.
    ed_visits = getattr(patient, "ed_visits", None) or []
    history.ed_visits = [v if hasattr(v, "visit_date") else EDVisitRecord(v) for v in ed_visits]
    return history
