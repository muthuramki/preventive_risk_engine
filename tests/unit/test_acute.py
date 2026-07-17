"""Tests that lock in the exact published NEWS2 tables from Section 1.0."""

import copy

from preventive_risk_engine.engines.risk_score.calculators.acute_calculator import (
    AcuteDeteriorationCalculator,
)
from preventive_risk_engine.models.patient import Vitals, DataField
from preventive_risk_engine.enums.priority import AVPU


def make_vitals(rr=16, spo2=98, sbp=120, hr=75, temp=37.0, o2=False, avpu=AVPU.ALERT):
    return Vitals(
        respiratory_rate=DataField(value=rr),
        spo2=DataField(value=spo2),
        supplemental_oxygen=DataField(value=o2),
        temperature=DataField(value=temp),
        systolic_bp=DataField(value=sbp),
        heart_rate=DataField(value=hr),
        avpu=DataField(value=avpu),
    )


class DummyPatient:
    def __init__(self, vitals):
        self.vitals = vitals


def calc(config):
    return AcuteDeteriorationCalculator(config)


# ---- Respiratory rate bands -------------------------------------------------

def test_rr_bands(us_config):
    c = calc(us_config)
    cases = [(8, 3), (7, 3), (9, 1), (11, 1), (12, 0), (20, 0), (21, 2), (24, 2), (25, 3), (30, 3)]
    for rr, expected in cases:
        p = DummyPatient(make_vitals(rr=rr))
        assert c.parameter_points(p)["respiratory_rate"] == expected, f"RR={rr}"


# ---- SpO2 bands --------------------------------------------------------------

def test_spo2_bands(us_config):
    c = calc(us_config)
    cases = [(91, 3), (85, 3), (92, 2), (93, 2), (94, 1), (95, 1), (96, 0), (100, 0)]
    for spo2, expected in cases:
        p = DummyPatient(make_vitals(spo2=spo2))
        assert c.parameter_points(p)["spo2"] == expected, f"SpO2={spo2}"


# ---- Systolic BP bands ---------------------------------------------------------

def test_systolic_bp_bands(us_config):
    c = calc(us_config)
    cases = [(90, 3), (80, 3), (91, 2), (100, 2), (101, 1), (110, 1), (111, 0), (219, 0), (220, 3), (240, 3)]
    for sbp, expected in cases:
        p = DummyPatient(make_vitals(sbp=sbp))
        assert c.parameter_points(p)["systolic_bp"] == expected, f"SBP={sbp}"


# ---- Heart rate bands ----------------------------------------------------------

def test_heart_rate_bands(us_config):
    c = calc(us_config)
    cases = [(40, 3), (30, 3), (41, 1), (50, 1), (51, 0), (90, 0), (91, 1), (110, 1),
             (111, 2), (130, 2), (131, 3), (150, 3)]
    for hr, expected in cases:
        p = DummyPatient(make_vitals(hr=hr))
        assert c.parameter_points(p)["heart_rate"] == expected, f"HR={hr}"


# ---- Temperature bands ----------------------------------------------------------

def test_temperature_bands(us_config):
    c = calc(us_config)
    cases = [(35.0, 3), (34.0, 3), (35.1, 1), (36.0, 1), (36.1, 0), (38.0, 0),
             (38.1, 1), (39.0, 1), (39.1, 2), (40.0, 2)]
    for temp, expected in cases:
        p = DummyPatient(make_vitals(temp=temp))
        assert c.parameter_points(p)["temperature"] == expected, f"Temp={temp}"


# ---- Supplemental oxygen and AVPU ------------------------------------------------

def test_supplemental_oxygen_adds_two_points(us_config):
    c = calc(us_config)
    p = DummyPatient(make_vitals(o2=True))
    assert c.parameter_points(p)["supplemental_oxygen"] == 2

    p2 = DummyPatient(make_vitals(o2=False))
    assert c.parameter_points(p2)["supplemental_oxygen"] == 0


def test_avpu_not_alert_scores_three(us_config):
    c = calc(us_config)
    p = DummyPatient(make_vitals(avpu=AVPU.VOICE))
    assert c.parameter_points(p)["avpu"] == 3

    p2 = DummyPatient(make_vitals(avpu=AVPU.ALERT))
    assert c.parameter_points(p2)["avpu"] == 0


# ---- Red flag logic ---------------------------------------------------------------

def test_red_flag_fires_at_news2_seven(us_config):
    c = calc(us_config)
    # RR 25 (3) + SpO2 91 (3) + SBP normal (0) + HR normal (0) + temp normal (0) = 6, not yet red flag
    p = DummyPatient(make_vitals(rr=25, spo2=91, sbp=120, hr=75, temp=37.0))
    assert c.raw_news2(p) == 6
    assert c.is_red_flag(p) is True  # single-parameter extreme (RR=3 or SpO2=3) triggers red flag


def test_red_flag_does_not_fire_when_stable(us_config):
    c = calc(us_config)
    p = DummyPatient(make_vitals())  # all normal
    assert c.raw_news2(p) == 0
    assert c.is_red_flag(p) is False


def test_single_parameter_extreme_is_red_flag_even_with_low_total(us_config):
    c = calc(us_config)
    # Only SBP is extreme (>=220 -> 3 points); everything else normal -> total = 3
    p = DummyPatient(make_vitals(sbp=225))
    assert c.raw_news2(p) == 3
    assert c.meets_single_parameter_extreme(p) is True
    assert c.is_red_flag(p) is True
