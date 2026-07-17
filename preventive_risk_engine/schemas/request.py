"""Request schema for POST /api/v1/patients/{patient_id}/risk-score/calculate
(Section 11)."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RiskScoreRequest:
    patient_id: str
    calculation_mode: str = "rules_v2"
    as_of_date: Optional[str] = None
    locale: str = "US"

    @classmethod
    def from_dict(cls, data: dict) -> "RiskScoreRequest":
        return cls(
            patient_id=data["patient_id"],
            calculation_mode=data.get("calculation_mode", "rules_v2"),
            as_of_date=data.get("as_of_date"),
            locale=data.get("locale", "US"),
        )
