"""
Patient and vitals models (Section 5 / Table 4).

Every field is wrapped in DataField so we can record value, timestamp,
source and unit, and tag it present / missing / stale, per the spec's
missing-data handling requirements (Section 13 / Table 11).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional

from preventive_risk_engine.enums.priority import AVPU
from preventive_risk_engine.enums.locale import Locale


@dataclass
class DataField:
    """Wraps a single clinical data point with provenance metadata."""
    value: Optional[Any] = None
    timestamp: Optional[datetime] = None
    source: Optional[str] = None
    unit: Optional[str] = None
    freshness_window: Optional[timedelta] = None  # e.g. 14 months for HbA1c

    @property
    def is_present(self) -> bool:
        return self.value is not None

    @property
    def is_stale(self) -> bool:
        if not self.is_present or self.timestamp is None or self.freshness_window is None:
            return False
        return (datetime.utcnow() - self.timestamp) > self.freshness_window

    @property
    def status(self) -> str:
        if not self.is_present:
            return "missing"
        if self.is_stale:
            return "stale"
        return "present"


@dataclass
class Vitals:
    """Section 1.0 / 7.1 — the seven NEWS2 inputs plus supporting trend data."""
    respiratory_rate: DataField = field(default_factory=DataField)   # breaths/min
    spo2: DataField = field(default_factory=DataField)               # %
    supplemental_oxygen: DataField = field(default_factory=DataField)  # bool
    temperature: DataField = field(default_factory=DataField)        # °C
    systolic_bp: DataField = field(default_factory=DataField)        # mmHg
    diastolic_bp: DataField = field(default_factory=DataField)       # mmHg
    heart_rate: DataField = field(default_factory=DataField)         # bpm
    avpu: DataField = field(default_factory=DataField)               # AVPU enum
    weight_kg: DataField = field(default_factory=DataField)          # for trend / HF weight-gain rule
    bmi: DataField = field(default_factory=DataField)
    glucose: DataField = field(default_factory=DataField)

    # Trend inputs (Section 7.1): adverse trends should raise the sub-score.
    rr_trend_rising: bool = False
    spo2_trend_falling: bool = False
    weight_gain_pct_last_week: Optional[float] = None  # for HF patients: >=5% is significant


@dataclass
class Demographics:
    age: int = 0
    sex: str = ""  # "male" / "female" / "other"
    location_region: Optional[str] = None
    payer_type: Optional[str] = None


@dataclass
class Patient:
    patient_id: str
    locale: Locale = Locale.US
    demographics: Demographics = field(default_factory=Demographics)
    vitals: Vitals = field(default_factory=Vitals)

    conditions: list = field(default_factory=list)          # list[ConditionRecord]
    admissions: list = field(default_factory=list)          # list[AdmissionRecord]
    medications: list = field(default_factory=list)         # list[MedicationRecord]
    labs: list = field(default_factory=list)                # list[LabResult]
    lifestyle: Optional[Any] = None                         # LifestyleProfile
    care_plan_tasks: list = field(default_factory=list)

    acute_symptom_flags: list = field(default_factory=list)  # e.g. ["chest_pain", "suicidal_ideation"]
    panic_lab_flags: list = field(default_factory=list)

    def snapshot(self) -> dict:
        """A JSON-serializable snapshot for the audit log (Section 14.2)."""
        return {
            "patient_id": self.patient_id,
            "locale": self.locale.value if isinstance(self.locale, Locale) else self.locale,
            "age": self.demographics.age,
            "sex": self.demographics.sex,
            "condition_count": len(self.conditions),
            "admission_count": len(self.admissions),
            "medication_count": len(self.medications),
        }
