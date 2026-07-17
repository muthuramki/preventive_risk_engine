# Preventive Care Patient Risk Scoring Engine

Rules-based, transparent, deterministic MVP implementation of the unified
clinical/developer specification. Every sub-score wraps a **published,
validated clinical instrument** — NEWS2, Charlson (chronic burden), LACE
(readmission), Beers/STOPP-START (medication risk), PDC (adherence),
HEDIS-style rules (care gaps), USPSTF/India schedules (preventive care),
and structured SDOH screening (lifestyle/social).

> **Not a diagnosis.** This tool prioritizes attention and surfaces
> signals. It must never auto-deny, auto-discharge, ration, or replace
> clinical judgment. All thresholds/weights are an initial expert proposal
> pending clinician sign-off (see Section 14 of the spec).

## Quickstart

```bash
pip install -r requirements.txt
python examples/risk_score_example.py
```

## Architecture (Section 3)

```
Red-flag check -> 8 sub-score calculators -> weighted aggregation
(renormalized over present data) -> confidence score -> explanation
(top-5 drivers) -> interventions + escalation -> audit log
```

See `docs/architecture.md` for the full pipeline diagram and
`preventive_risk_engine/engines/risk_score/pipeline.py` for the
implementation, which mirrors Appendix B's pseudocode line-for-line.

## Key entry point

```python
from preventive_risk_engine import score_patient

result = score_patient(patient)          # patient: models.patient.Patient
print(result.to_api_response())          # matches Section 11's JSON contract
```

## Configuration

All clinical thresholds live in `preventive_risk_engine/resources/`:

- `scoring_config.yaml` — sub-score weights, red-flag thresholds, NEWS2 tables
- `locale_us.yaml` / `locale_india.yaml` — units, guideline targets, screening schedules

Change values there — never hard-code clinical thresholds in Python.

## Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

## Status

Draft for clinical validation — **not approved for clinical use**.
