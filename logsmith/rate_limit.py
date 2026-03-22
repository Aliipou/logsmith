"""Rate-limited logging to prevent log storms from hot paths."""
from __future__ import annotations
import logging
import time
from collections import defaultdict


class RateLimitedLogger:
    """Wraps a logger and suppresses repeated messages within a time window.

    Useful for hot code paths (tight loops, high-frequency events) where
    a single bug could flood your log aggregation pipeline.

    Usage::

        logger = RateLimitedLogger(logsmith.get_logger(__name__), rate=1, per=60)
        # Logs at most once per minute per unique message
        for item in huge_list:
            logger.warning("item has no price", extra={"item_id": item.id})
    """

    def __init__(self, logger: logging.Logger, rate: int = 1, per: float = 60.0) -> None:
        self._logger = logger
        self._rate = rate
        self._per = per
        self._counts: dict[str, list[float]] = defaultdict(list)

    def _is_allowed(self, key: str) -> bool:
        now = time.monotonic()
        window = self._counts[key]
        window[:] = [t for t in window if now - t < self._per]
        if len(window) < self._rate:
            window.append(now)
            return True
        return False

    def warning(self, msg: str, **kwargs) -> None:
        if self._is_allowed(msg):
            self._logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        if self._is_allowed(msg):
            self._logger.error(msg, **kwargs)

    def info(self, msg: str, **kwargs) -> None:
        if self._is_allowed(msg):
            self._logger.info(msg, **kwargs)
