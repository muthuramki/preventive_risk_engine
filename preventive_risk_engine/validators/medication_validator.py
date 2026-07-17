"""Validation for medication records feeding the Beers/STOPP-START calculator."""

from typing import Any, List

from preventive_risk_engine.base.base_validator import BaseValidator


class MedicationValidator(BaseValidator):
    def validate(self, data: Any) -> List[str]:
        errors: List[str] = []
        meds = getattr(data, "medications", None)
        if meds is None:
            return errors  # absence is valid -- calculator marks sub-score missing
        for i, m in enumerate(meds):
            if not getattr(m, "name", None):
                errors.append(f"medications[{i}].name is required")
        return errors
