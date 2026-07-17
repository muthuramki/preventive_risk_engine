"""Weighted aggregation, renormalized over present data (Section 8).

    overall = SUM(subscore_i * weight_i) / SUM(weight_i present)   // capped at 100

Missing sub-scores are excluded entirely -- never treated as 0 (false
reassurance) or 100 (false alarm).
"""

from typing import Dict, Optional

from preventive_risk_engine.base.base_aggregator import BaseAggregator
from preventive_risk_engine.exceptions.calculator_exception import CalculatorError


class WeightedAggregator(BaseAggregator):
    def aggregate(self, sub_scores: Dict[str, Optional[float]], weights: Dict[str, float]) -> float:
        present = {k: v for k, v in sub_scores.items() if v is not None}
        if not present:
            raise CalculatorError(
                "No sub-scores were computable; cannot aggregate an overall score. "
                "This should route to 'needs review', not a default score."
            )

        total_weight = sum(weights[k] for k in present if k in weights)
        if total_weight <= 0:
            raise CalculatorError("Total weight over present sub-scores is zero.")

        weighted_sum = sum(present[k] * weights[k] for k in present if k in weights)
        overall = weighted_sum / total_weight
        return min(100.0, max(0.0, overall))

    @staticmethod
    def completeness_pct(sub_scores: Dict[str, Optional[float]]) -> float:
        if not sub_scores:
            return 0.0
        present = sum(1 for v in sub_scores.values() if v is not None)
        return round(100.0 * present / len(sub_scores), 1)
