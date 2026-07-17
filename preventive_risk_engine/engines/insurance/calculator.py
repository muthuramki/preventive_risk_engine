"""Maps a clinical RiskResult onto an illustrative insurance risk band.
This is a scaffold, not a validated actuarial model -- do not use for
underwriting decisions without actuarial and regulatory review."""


def insurance_band(overall_score, config) -> str:
    if overall_score is None:
        return "Needs Review"
    if overall_score >= config.high_risk_score_threshold:
        return "High Utilization Risk"
    return "Standard"
