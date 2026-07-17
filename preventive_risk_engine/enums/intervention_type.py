from enum import Enum


class RecipientRole(str, Enum):
    """Section 10 / Table 9 — role-specific outputs."""
    PATIENT = "patient"
    DOCTOR = "doctor"
    NURSE = "registered_nurse"
    CARE_COORDINATOR = "care_coordinator"
    PHARMACIST = "pharmacist"


class InterventionCategory(str, Enum):
    REVIEW_QUEUE = "review_queue"
    MONITORING_TASK = "monitoring_task"
    GAP_CLOSURE = "gap_closure"
    SOCIAL_RESOURCE = "social_resource"
    MEDICATION_RECONCILIATION = "medication_reconciliation"
    PATIENT_EDUCATION = "patient_education"
