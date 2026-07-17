"""Response schema helpers matching Section 11's JSON contract.

RiskResult.to_api_response() already produces this shape; this module just
documents the contract and offers a light validation helper."""

REQUIRED_RESPONSE_FIELDS = [
    "patient_id", "risk_score", "risk_level", "red_flag", "data_confidence",
    "sub_scores", "instrument_provenance", "top_risk_drivers",
    "screening_gaps", "recommended_actions", "escalation_level",
    "rules_version", "locale", "disclaimer",
]


def validate_response_shape(response: dict) -> list:
    return [f for f in REQUIRED_RESPONSE_FIELDS if f not in response]
