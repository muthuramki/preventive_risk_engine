"""Unit conversion helpers for US/India locale packs (Section 14.1)."""


def mgdl_to_mmol_l_glucose(mgdl: float) -> float:
    return round(mgdl / 18.0182, 2)


def mmol_l_to_mgdl_glucose(mmol: float) -> float:
    return round(mmol * 18.0182, 1)


def celsius_to_fahrenheit(c: float) -> float:
    return round((c * 9 / 5) + 32, 1)


def fahrenheit_to_celsius(f: float) -> float:
    return round((f - 32) * 5 / 9, 1)


def kg_to_lb(kg: float) -> float:
    return round(kg * 2.20462, 1)


def lb_to_kg(lb: float) -> float:
    return round(lb / 2.20462, 1)
