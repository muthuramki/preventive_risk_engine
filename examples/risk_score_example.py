"""
Runnable example implementing the spec's Section 8.2 worked scenario:

    64-year-old female, T2DM + HTN + HF + CKD stage 3, 2 admissions in 6
    months including a 30-day readmission, 8 active meds incl. a blood
    thinner and insulin, HbA1c overdue, PDC ~70%, transport barrier + lives
    alone, vitals stable (NEWS2 = 2).

Run with:  python examples/risk_score_example.py
"""

import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from preventive_risk_engine.enums.locale import Locale
from preventive_risk_engine.enums.disease_type import ChronicCondition
from preventive_risk_engine.enums.priority import AVPU

from preventive_risk_engine.models.patient import Patient, Demographics, Vitals, DataField
from preventive_risk_engine.models.admission import ConditionRecord, AdmissionRecord
from preventive_risk_engine.models.medication import MedicationRecord, AdherenceRecord
from preventive_risk_engine.models.lifestyle import LifestyleProfile
from preventive_risk_engine.models.lab import ScreeningGap

from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.engines.risk_score.engine import RiskScoreEngine


def build_example_patient() -> Patient:
    today = date.today()

    patient = Patient(
        patient_id="P10001",
        locale=Locale.US,
        demographics=Demographics(age=64, sex="female", location_region="US-CA"),
        vitals=Vitals(
            respiratory_rate=DataField(value=60, unit="breaths/min"),
            spo2=DataField(value=97, unit="%"),
            supplemental_oxygen=DataField(value=False),
            temperature=DataField(value=36.8, unit="C"),
            systolic_bp=DataField(value=128, unit="mmHg"),
            diastolic_bp=DataField(value=78, unit="mmHg"),
            heart_rate=DataField(value=82, unit="bpm"),
            avpu=DataField(value=AVPU.ALERT),
        ),
    )

    patient.conditions = [
        ConditionRecord(condition=ChronicCondition.DIABETES, active=True),
        ConditionRecord(condition=ChronicCondition.HYPERTENSION, active=True),
        ConditionRecord(condition=ChronicCondition.HEART_FAILURE, active=True),
        ConditionRecord(condition=ChronicCondition.CKD_STAGE_1_3, active=True, severity="stage_3"),
    ]

    patient.admissions = [
        AdmissionRecord(admission_date=today - timedelta(days=150), was_30_day_readmission=True),
        AdmissionRecord(admission_date=today - timedelta(days=60), was_30_day_readmission=False),
    ]

    patient.medications = [
        MedicationRecord(name="Warfarin", drug_class="anticoagulant", is_beers_listed=True),
        MedicationRecord(name="Insulin glargine", drug_class="insulin", is_beers_listed=True),
        MedicationRecord(name="Lisinopril"),
        MedicationRecord(name="Metoprolol"),
        MedicationRecord(name="Furosemide"),
        MedicationRecord(name="Metformin"),
        MedicationRecord(name="Atorvastatin"),
        MedicationRecord(name="Aspirin"),
    ]

    # PDC ~70% -> below the 80% threshold, above the 50% threshold.
    patient.adherence = AdherenceRecord(days_covered=63, days_in_window=90)
    patient.missed_appointments_6m = 1
    patient.missed_or_declined_critical_tasks = 0

    patient.lifestyle = LifestyleProfile(
        current_smoker=False,
        heavy_alcohol_use=False,
        transport_barrier=True,
        social_isolation=True,
    )

    patient.screening_gaps = [
        ScreeningGap(key="diabetic_hba1c", category="care_gap", status="overdue"),
        ScreeningGap(key="diabetic_eye_exam", category="care_gap", status="overdue"),
        ScreeningGap(key="colorectal", category="preventive_care", status="overdue"),
    ]

    return patient


def main():
    patient = build_example_patient()
    config = load_rules_config(locale=patient.locale)
    engine = RiskScoreEngine(config)
    result = engine.run(patient)

    print("=" * 70)
    print(f"Patient:            {result.patient_id}")
    print(f"Red flag:           {result.red_flag}")
    print(f"Overall score:      {result.overall_score}")
    print(f"Risk level:         {result.risk_level.value if result.risk_level else None}")
    print(f"Data confidence:    {result.data_confidence.value if result.data_confidence else None}")
    print(f"Escalation:         {result.escalation_level.value if result.escalation_level else None}")
    print("-" * 70)
    print("Sub-scores:")
    for key, sub in result.sub_scores.items():
        print(f"  {key:28s} = {sub.value}  (instrument: {sub.instrument})")
    print("-" * 70)
    print("Top 5 drivers:")
    for d in result.top_risk_drivers:
        print(f"  - {d}")
    print("-" * 70)
    print("Recommended actions by role:")
    for role, actions in result.recommended_actions.items():
        print(f"  {role}:")
        for a in actions:
            print(f"    - {a}")
    print("=" * 70)
    print(result.to_api_response())


if __name__ == "__main__":
    main()
