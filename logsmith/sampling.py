"""Probabilistic log sampling for high-volume production endpoints."""
from __future__ import annotations
import logging
import random


class SamplingFilter(logging.Filter):
    """Logging filter that samples records at a configurable rate.

    Useful for very high-throughput endpoints where logging every request
    would overwhelm your log pipeline, but you still want statistical coverage.

    Usage::

        # Log 10% of DEBUG records, 100% of WARNING+
        filter = SamplingFilter(rate=0.10, min_level=logging.WARNING)
        logging.getLogger("api.access").addFilter(filter)
    """

    def __init__(self, rate: float = 1.0, min_level: int = logging.WARNING) -> None:
        super().__init__()
        if not 0.0 <= rate <= 1.0:
            raise ValueError(f"rate must be in [0.0, 1.0], got {rate}")
        self._rate = rate
        self._min_level = min_level

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno >= self._min_level:
            return True
        return random.random() < self._rate
