"""Validation for admission/utilization records feeding the LACE calculator."""

from typing import Any, List

from preventive_risk_engine.base.base_validator import BaseValidator


class AdmissionValidator(BaseValidator):
    def validate(self, data: Any) -> List[str]:
        errors: List[str] = []
        admissions = getattr(data, "admissions", None)
        if admissions is None:
            return errors
        for i, a in enumerate(admissions):
            if getattr(a, "admission_date", None) is None:
                errors.append(f"admissions[{i}].admission_date is required")
        return errors
