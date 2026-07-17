# Sub-score calculators

Each wraps a published clinical instrument and returns 0-100 (Section 7):

| Key | Instrument | File |
|---|---|---|
| acute_deterioration | NEWS2 | calculators/acute_calculator.py |
| chronic_disease_burden | Charlson Comorbidity Index | calculators/chronic_calculator.py |
| hospital_readmission | LACE index | calculators/readmission_calculator.py |
| medication | Beers / STOPP-START + polypharmacy | calculators/medication_calculator.py |
| compliance_adherence | PDC | calculators/adherence_calculator.py |
| lifestyle_social | SDOH screening | calculators/lifestyle_calculator.py |
| care_gap | HEDIS-style rules | calculators/care_gap_calculator.py |
| preventive_care | USPSTF / India schedules | calculators/preventive_calculator.py |

All thresholds are clinician-tunable via `resources/scoring_config.yaml`.
