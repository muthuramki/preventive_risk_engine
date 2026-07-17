"""Lab results and screening-gap models (Section 7.6/7.7, Appendix A)."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class LabResult:
    name: str  # e.g. "HbA1c", "creatinine", "eGFR"
    value: Optional[float] = None
    unit: Optional[str] = None
    result_date: Optional[date] = None
    is_panic_value: bool = False
    is_imputed: bool = False


@dataclass
class ScreeningGap:
    key: str                 # e.g. "diabetic_hba1c", "colorectal"
    category: str            # "care_gap" | "preventive_care"
    status: str              # "overdue" | "due_soon" | "up_to_date" | "not_applicable"
    last_done_date: Optional[date] = None
    recommended_interval_days: Optional[int] = None
