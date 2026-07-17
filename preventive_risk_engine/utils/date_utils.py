"""Date helpers: freshness windows, recency weighting."""

from datetime import date, datetime, timedelta
from typing import Optional


def days_since(d: Optional[date], as_of: Optional[date] = None) -> Optional[int]:
    if d is None:
        return None
    as_of = as_of or date.today()
    return (as_of - d).days


def is_stale(timestamp: Optional[datetime], window: timedelta) -> bool:
    if timestamp is None:
        return False
    return (datetime.utcnow() - timestamp) > window
