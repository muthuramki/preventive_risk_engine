"""Validation for the incoming API request payload (Section 11)."""

from typing import Any, List

from preventive_risk_engine.base.base_validator import BaseValidator


class RequestValidator(BaseValidator):
    ALLOWED_LOCALES = {"US", "India"}

    def validate(self, data: Any) -> List[str]:
        errors: List[str] = []
        patient_id = data.get("patient_id") if isinstance(data, dict) else getattr(data, "patient_id", None)
        if not patient_id:
            errors.append("patient_id is required")
        locale = data.get("locale") if isinstance(data, dict) else getattr(data, "locale", None)
        if locale and locale not in self.ALLOWED_LOCALES:
            errors.append(f"locale must be one of {sorted(self.ALLOWED_LOCALES)}")
        return errors
