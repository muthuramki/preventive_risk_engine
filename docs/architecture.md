# Architecture Overview (Section 3)

```
Patient data
     |
     v
[1] Red-flag override check (vitals, labs, acute symptoms)
     |  -- if triggered --> CRITICAL / Emergency escalation (short-circuit)
     v
[2] Eight sub-score calculators (0-100 each, validated instruments)
     v
[3] Weighted aggregation -> Overall 0-100 (renormalized over present data)
     v
[4] Data-completeness / confidence score
     v
[5] Explanation engine (top-5 drivers)
     v
[6] Intervention + escalation mapping (role-specific)
     v
[7] Immutable audit log
```

Code mapping:

| Stage | Module |
|---|---|
| 1 | `engines/risk_score/red_flag_engine.py` |
| 2 | `engines/risk_score/calculators/*.py` |
| 3 | `engines/risk_score/aggregator.py` |
| 4 | `enums/risk_level.py` (`DataConfidence`) |
| 5 | `engines/risk_score/explanation_engine.py` |
| 6 | `engines/risk_score/intervention_engine.py`, `escalation_engine.py` |
| 7 | left to the service/audit layer (out of scope for this package) |

Orchestration entry point: `engines/risk_score/pipeline.py` (`RiskScorePipeline.run`),
which mirrors Appendix B's pseudocode.
