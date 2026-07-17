"""Preventive Care Patient Risk Scoring Engine.

Rules-based, transparent, deterministic MVP implementing the unified
clinical/developer specification. Wraps published instruments (NEWS2,
Charlson, LACE, Beers/STOPP-START, PDC, HEDIS, USPSTF/India schedules,
SDOH screening) rather than inventing new medical math.

NOT A DIAGNOSIS. Supports clinician review; must never auto-deny,
auto-discharge, ration, or replace clinical judgment. Every threshold and
weight here is an initial expert proposal pending clinician sign-off.
"""

from preventive_risk_engine.version import __version__, RULES_VERSION
from preventive_risk_engine.engines.risk_score.orchestrator import score_patient

__all__ = ["__version__", "RULES_VERSION", "score_patient"]
