"""Placeholder -- see Section 18 (Post-MVP predictive analytics roadmap)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from preventive_risk_engine.engines.prediction.engine import PredictionEngine

if __name__ == "__main__":
    engine = PredictionEngine()
    print(engine.run(features={}))
