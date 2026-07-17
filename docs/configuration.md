# Configuration

- `resources/scoring_config.yaml` — weights, red-flag thresholds, NEWS2 tables
- `resources/locale_us.yaml` / `locale_india.yaml` — units, guideline targets, screening schedules

Load with `preventive_risk_engine.config.loader.load_rules_config(locale=...)`.
Never hard-code a clinical threshold in Python — add it to YAML instead.
