"""Schema for role-based recommended actions payload."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InterventionSchema:
    recommended_actions: Dict[str, List[str]] = field(default_factory=dict)
