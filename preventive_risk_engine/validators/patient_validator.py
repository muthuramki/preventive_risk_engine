"""Structural validation for Patient objects before scoring (Section 13)."""

from typing import Any, List

from preventive_risk_engine.base.base_validator import BaseValidator


class PatientValidator(BaseValidator):
    def validate(self, data: Any) -> List[str]:
        errors: List[str] = []
        if not getattr(data, "patient_id", None):
            errors.append("patient_id is required")
        if getattr(data, "demographics", None) is None:
            errors.append("demographics block is required")
        else:
            age = getattr(data.demographics, "age", None)
            if age is None or age < 0 or age > 130:
                errors.append("demographics.age must be a plausible human age")
        if getattr(data, "vitals", None) is None:
            errors.append("vitals block is required (even if all fields are missing/None)")
        return errors
