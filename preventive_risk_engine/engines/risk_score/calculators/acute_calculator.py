"""
Acute deterioration sub-score, derived from NEWS2 (Section 7.1).

Pipeline:
  1. Score each of the 7 NEWS2 parameters via published lookup tables.
  2. Sum -> NEWS2 total (0-20+).
  3. Map the NEWS2 total (plus adverse-trend nudges) onto the internal
     0-100 sub-score scale.
  4. Separately expose whether this patient meets the red-flag criteria
     (NEWS2 >= 7, or any single parameter scoring the max 3 points) so the
     red_flag_engine can short-circuit the pipeline (Section 7.9).

This calculator only implements the *scoring*, not the override decision --
that lives in red_flag_engine.py, which calls `raw_news2()` /
`meets_single_parameter_extreme()` on this same object to stay
DRY and avoid re-implementing the lookup tables twice.
"""

from typing import Any, Dict

from preventive_risk_engine.base.base_calculator import BaseCalculator
from preventive_risk_engine.enums.priority import AVPU
from preventive_risk_engine.config.constants.risk_constants import (
    RESPIRATORY_RATE_BANDS,
    SPO2_BANDS,
    SYSTOLIC_BP_BANDS,
    HEART_RATE_BANDS,
    TEMPERATURE_BANDS,
    SUPPLEMENTAL_OXYGEN_POINTS,
    AVPU_ALERT_POINTS,
    AVPU_NOT_ALERT_POINTS,
    NEWS2_BAND_THRESHOLDS,
    NEWS2_RED_FLAG_THRESHOLD,
)


class AcuteDeteriorationCalculator(BaseCalculator):
    key = "acute_deterioration"
    instrument = "NEWS2"

    # A NEWS2 sub-score of 3 in *any single* parameter is itself an escalation
    # trigger per standard NEWS2 clinical protocol, independent of the total.
    SINGLE_PARAM_EXTREME = 3

    def is_computable(self, patient: Any) -> bool:
        v = patient.vitals
        # We need at minimum RR, SpO2, systolic BP, HR and temperature to
        # produce a clinically meaningful NEWS2. AVPU/O2 default sensibly
        # (Alert / no supplemental O2) if genuinely not captured, but the
        # five core vitals must be present -- otherwise this is "missing",
        # not "assume stable" (Section 13: never default to false reassurance).
        required = [v.respiratory_rate, v.spo2, v.systolic_bp, v.heart_rate, v.temperature]
        return all(f.is_present for f in required)

    def parameter_points(self, patient: Any) -> Dict[str, int]:
        v = patient.vitals
        points = {
            "respiratory_rate": self.lookup_band(float(v.respiratory_rate.value), RESPIRATORY_RATE_BANDS),
            "spo2": self.lookup_band(float(v.spo2.value), SPO2_BANDS),
            "systolic_bp": self.lookup_band(float(v.systolic_bp.value), SYSTOLIC_BP_BANDS),
            "heart_rate": self.lookup_band(float(v.heart_rate.value), HEART_RATE_BANDS),
            "temperature": self.lookup_band(float(v.temperature.value), TEMPERATURE_BANDS),
        }

        # Supplemental oxygen: +2 flat, regardless of SpO2 value.
        on_o2 = bool(v.supplemental_oxygen.value) if v.supplemental_oxygen.is_present else False
        points["supplemental_oxygen"] = SUPPLEMENTAL_OXYGEN_POINTS if on_o2 else 0

        # AVPU: Alert -> 0, anything else (new confusion/Voice/Pain/Unresponsive) -> 3.
        if v.avpu.is_present:
            avpu_value = v.avpu.value
            is_alert = (avpu_value == AVPU.ALERT) or (avpu_value == AVPU.ALERT.value)
            points["avpu"] = AVPU_ALERT_POINTS if is_alert else AVPU_NOT_ALERT_POINTS
        else:
            # Not captured: treat conservatively as Alert (0) rather than
            # penalizing for a missing field, but this should surface as a
            # data-completeness gap upstream, not silently assumed forever.
            points["avpu"] = AVPU_ALERT_POINTS

        return points

    def raw_news2(self, patient: Any) -> int:
        return sum(self.parameter_points(patient).values())

    def meets_single_parameter_extreme(self, patient: Any) -> bool:
        return any(p >= self.SINGLE_PARAM_EXTREME for p in self.parameter_points(patient).values())

    def news2_band(self, total: int) -> str:
        for low, high, band in NEWS2_BAND_THRESHOLDS:
            if low <= total <= high:
                return band
        return "critical"

    def is_red_flag(self, patient: Any) -> bool:
        """Section 7.9: NEWS2 >= 7, OR any single parameter at the extreme."""
        if not self.is_computable(patient):
            return False
        total = self.raw_news2(patient)
        return total >= NEWS2_RED_FLAG_THRESHOLD or self.meets_single_parameter_extreme(patient)

    def _compute_raw(self, patient: Any) -> float:
        total = self.raw_news2(patient)

        # Map NEWS2's 0-20(+) scale onto the internal 0-100 scale.
        # NEWS2 rarely exceeds ~20 in practice; we treat 20 as the practical
        # ceiling for a proportional mapping, then apply trend nudges.
        news2_ceiling = 20
        base = min(100.0, (total / news2_ceiling) * 100.0)

        # Adverse-trend nudges (Section 7.1): rising RR, falling SpO2, or
        # >=5% weekly weight gain in a heart-failure patient push the score
        # up even if the instantaneous NEWS2 total looks stable.
        v = patient.vitals
        trend_bump = 0.0
        if v.rr_trend_rising:
            trend_bump += 5.0
        if v.spo2_trend_falling:
            trend_bump += 5.0
        if v.weight_gain_pct_last_week is not None and v.weight_gain_pct_last_week >= 5.0:
            trend_bump += 10.0

        return base + trend_bump
