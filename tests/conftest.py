import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from preventive_risk_engine.config.loader import load_rules_config
from preventive_risk_engine.enums.locale import Locale
from preventive_risk_engine.models.patient import Patient, Demographics, Vitals, DataField
from preventive_risk_engine.enums.priority import AVPU


@pytest.fixture
def us_config():
    return load_rules_config(locale=Locale.US)


@pytest.fixture
def stable_patient():
    return Patient(
        patient_id="TEST-001",
        locale=Locale.US,
        demographics=Demographics(age=50, sex="female"),
        vitals=Vitals(
            respiratory_rate=DataField(value=16),
            spo2=DataField(value=98),
            supplemental_oxygen=DataField(value=False),
            temperature=DataField(value=37.0),
            systolic_bp=DataField(value=120),
            heart_rate=DataField(value=75),
            avpu=DataField(value=AVPU.ALERT),
        ),
    )
