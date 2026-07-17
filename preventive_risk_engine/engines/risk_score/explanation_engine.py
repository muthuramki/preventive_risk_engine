"""Plain-language top-5 driver explanations (Section 10).

MVP heuristic: rank sub-scores by their *weighted contribution*
(value * weight), then render a human-readable phrase for each of the
top-scoring categories. A production system would swap in richer,
rule-specific reason codes per calculator; this keeps the contract stable."""

from typing import Any, Dict, List, Optional

from preventive_risk_engine.base.base_explainer import BaseExplainer

DRIVER_PHRASES = {
    "acute_deterioration": "Vital signs indicate acute deterioration risk (NEWS2)",
    "chronic_disease_burden": "High chronic disease burden / multimorbidity",
    "hospital_readmission": "Recent hospital or ED utilization / readmission risk",
    "medication": "Medication risk: polypharmacy or high-risk medications",
    "compliance_adherence": "Sub-target medication adherence or missed appointments",
    "lifestyle_social": "Social/lifestyle risk factors (SDOH) needing support",
    "care_gap": "Open guideline-recommended care gaps",
    "preventive_care": "Overdue preventive screening or immunization",
}


class ExplanationEngine(BaseExplainer):
    def top_drivers(self, sub_scores: Dict[str, Optional[float]], patient: Any, n: int = 5) -> List[str]:
        weights = self.config.weights if hasattr(self, "config") else None
        ranked = []
        for key, value in sub_scores.items():
            if value is None:
                continue
            weight = self.config.weight(key) if hasattr(self, "config") else 1
            ranked.append((value * weight, key, value))

        ranked.sort(key=lambda t: t[0], reverse=True)
        drivers = [DRIVER_PHRASES.get(key, key) for _, key, _ in ranked[:n]]
        return drivers

    def __init__(self, config: Any):
        self.config = config
