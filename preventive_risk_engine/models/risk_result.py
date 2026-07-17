"""The full output of one risk-scoring run (Section 8 / 11)."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from preventive_risk_engine.enums.risk_level import RiskLevel, DataConfidence
from preventive_risk_engine.enums.priority import EscalationTier


@dataclass
class SubScoreResult:
    key: str
    value: Optional[float]           # 0-100, None if not computable
    weight: float
    instrument: str                  # provenance, e.g. "NEWS2"
    present: bool = True
    detail: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedFlag:
    code: str
    description: str
    source: str  # e.g. "NEWS2", "panic_lab", "acute_symptom"


@dataclass
class RiskResult:
    patient_id: str
    rules_version: str
    locale: str

    overall_score: Optional[float] = None      # None when a red flag short-circuits scoring
    risk_level: Optional[RiskLevel] = None
    red_flag: bool = False
    red_flags: List[RedFlag] = field(default_factory=list)

    sub_scores: Dict[str, SubScoreResult] = field(default_factory=dict)
    data_confidence: Optional[DataConfidence] = None
    completeness_pct: Optional[float] = None

    top_risk_drivers: List[str] = field(default_factory=list)
    screening_gaps: List[Dict[str, Any]] = field(default_factory=list)
    recommended_actions: Dict[str, List[str]] = field(default_factory=dict)  # by role
    escalation_level: Optional[EscalationTier] = None

    disclaimer: str = "Supports clinical review; does not replace judgment."

    def to_api_response(self) -> Dict[str, Any]:
        """Shape matching Section 11's JSON contract."""
        return {
            "patient_id": self.patient_id,
            "risk_score": round(self.overall_score) if self.overall_score is not None else None,
            "risk_level": self.risk_level.value if self.risk_level else "Critical",
            "red_flag": self.red_flag,
            "data_confidence": self.data_confidence.value if self.data_confidence else None,
            "sub_scores": {k: v.value for k, v in self.sub_scores.items()},
            "instrument_provenance": {k: v.instrument for k, v in self.sub_scores.items()},
            "top_risk_drivers": self.top_risk_drivers,
            "screening_gaps": self.screening_gaps,
            "recommended_actions": self.recommended_actions,
            "escalation_level": self.escalation_level.value if self.escalation_level else None,
            "rules_version": self.rules_version,
            "locale": self.locale,
            "disclaimer": self.disclaimer,
        }
