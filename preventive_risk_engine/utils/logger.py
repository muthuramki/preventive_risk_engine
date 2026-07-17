"""Standard logging setup for the engine (not the immutable clinical audit
log -- see docs/architecture.md for that distinction)."""

import logging
from typing import Optional

_LOGGER_NAME = "preventive_risk_engine"


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or _LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
