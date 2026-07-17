import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from preventive_risk_engine.engines.bmi.engine import BMIEngine

if __name__ == "__main__":
    engine = BMIEngine()
    print(engine.run(weight_kg=70, height_m=1.75))
