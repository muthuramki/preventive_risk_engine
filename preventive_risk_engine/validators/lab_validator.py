"""Validation for lab result records."""

from typing import Any, List

from preventive_risk_engine.base.base_validator import BaseValidator


class LabValidator(BaseValidator):
    def validate(self, data: Any) -> List[str]:
        errors: List[str] = []
        labs = getattr(data, "labs", None)
        if labs is None:
            return errors
        for i, lab in enumerate(labs):
            if not getattr(lab, "name", None):
                errors.append(f"labs[{i}].name is required")
        return errors
