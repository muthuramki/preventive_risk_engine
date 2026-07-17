"""Structured questionnaire wrapper, e.g. for SDOH intake forms."""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Optional


@dataclass
class QuestionnaireResponse:
    questionnaire_key: str
    responses: Dict[str, Any] = field(default_factory=dict)
    completed_date: Optional[date] = None
