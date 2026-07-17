"""Role-based recommended actions (Section 10 / Table 9).

Recommendations are suggestions for the care team, never auto-actions.
SDOH-derived recommendations must only ever ADD support resources, never
reduce a patient's priority (Table 6 equity guardrail).
"""

from typing import Any, Dict, List, Optional

from preventive_risk_engine.base.base_intervention import BaseIntervention
from preventive_risk_engine.enums.risk_level import RiskLevel
from preventive_risk_engine.enums.intervention_type import RecipientRole


class InterventionEngine(BaseIntervention):
    def recommend(
        self,
        risk_level: Optional[RiskLevel],
        sub_scores: Dict[str, Any],
        patient: Any,
    ) -> Dict[str, List[str]]:
        actions: Dict[str, List[str]] = {role.value: [] for role in RecipientRole}

        level = risk_level.value if risk_level else "Critical"

        if level in ("High", "Critical"):
            actions[RecipientRole.DOCTOR.value].append(
                f"Physician review within {'24 hours' if level == 'Critical' else '7 days'}."
            )
        if level in ("Mild", "Moderate"):
            actions[RecipientRole.NURSE.value].append("Nurse assessment and care-plan update.")

        care_gap = sub_scores.get("care_gap")
        if care_gap and care_gap > 0:
            actions[RecipientRole.CARE_COORDINATOR.value].append("Close open guideline-recommended care gaps.")
            actions[RecipientRole.PATIENT.value].append("Schedule overdue screenings/exams noted by your care team.")

        preventive = sub_scores.get("preventive_care")
        if preventive and preventive > 0:
            actions[RecipientRole.CARE_COORDINATOR.value].append("Schedule overdue preventive screenings/immunizations.")

        medication = sub_scores.get("medication")
        if medication and medication > 0:
            actions[RecipientRole.PHARMACIST.value].append("Medication reconciliation and Beers/interaction review.")

        adherence = sub_scores.get("compliance_adherence")
        if adherence and adherence > 0:
            actions[RecipientRole.PHARMACIST.value].append("Adherence support / refill-barrier review.")
            actions[RecipientRole.PATIENT.value].append("Discuss any barriers to taking medications as prescribed.")

        lifestyle = sub_scores.get("lifestyle_social")
        if lifestyle and lifestyle > 0:
            # Equity guardrail: route to support resources only.
            actions[RecipientRole.CARE_COORDINATOR.value].append(
                "Connect patient with social-resource support (transport/food/isolation) -- do not lower priority."
            )

        acute = sub_scores.get("acute_deterioration")
        if acute and acute >= 60:
            actions[RecipientRole.NURSE.value].append("Repeat/escalate vitals monitoring and symptom reassessment.")

        # Drop empty role lists for a cleaner response.
        return {role: acts for role, acts in actions.items() if acts}
