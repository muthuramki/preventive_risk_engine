"""Red-flag override checks (Section 7.9).

These sit OUTSIDE the weighted average by design: a weighted mean would
dangerously dilute a single life-threatening signal (e.g. SpO2 of 86%).
If any red flag fires, the pipeline short-circuits straight to emergency
escalation regardless of the numeric band (Section 8).
"""

from typing import Any, List

from preventive_risk_engine.models.risk_result import RedFlag
from preventive_risk_engine.engines.risk_score.calculators.acute_calculator import (
    AcuteDeteriorationCalculator,
)


class RedFlagEngine:
    def __init__(self, config: Any):
        self.config = config
        self._acute_calc = AcuteDeteriorationCalculator(config)

    def check(self, patient: Any) -> List[RedFlag]:
        flags: List[RedFlag] = []

        # 1. NEWS2 >= 7, or any single parameter at an extreme.
        if self._acute_calc.is_computable(patient) and self._acute_calc.is_red_flag(patient):
            total = self._acute_calc.raw_news2(patient)
            flags.append(RedFlag(
                code="NEWS2_CRITICAL",
                description=f"NEWS2 total = {total} (>= {self.config.red_flags.news2_critical_threshold}) "
                            f"or a single vital parameter at an extreme.",
                source="NEWS2",
            ))

        # 2. SpO2 below configured critical threshold (belt-and-suspenders
        #    with the NEWS2 check above, in case NEWS2 itself isn't computable
        #    but SpO2 alone is known).
        spo2_field = patient.vitals.spo2
        if spo2_field.is_present and float(spo2_field.value) <= self.config.red_flags.spo2_critical_threshold:
            flags.append(RedFlag(
                code="SPO2_CRITICAL",
                description=f"SpO2 {spo2_field.value}% at/below critical threshold "
                            f"({self.config.red_flags.spo2_critical_threshold}%).",
                source="vitals",
            ))

        # 3. Panic lab values.
        for lab_flag in getattr(patient, "panic_lab_flags", []) or []:
            flags.append(RedFlag(
                code="PANIC_LAB",
                description=f"Panic-value lab result: {lab_flag}.",
                source="labs",
            ))

        # 4. Documented acute symptom flags.
        for symptom in getattr(patient, "acute_symptom_flags", []) or []:
            if symptom in self.config.red_flags.acute_symptom_flags:
                flags.append(RedFlag(
                    code="ACUTE_SYMPTOM",
                    description=f"Documented acute symptom flag: {symptom}.",
                    source="clinical_note",
                ))

        # De-duplicate by code, keep first occurrence.
        seen = set()
        deduped = []
        for f in flags:
            if f.code not in seen:
                seen.add(f.code)
                deduped.append(f)
        return deduped
