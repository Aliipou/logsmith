"""Tests for RateLimitedLogger — rate limiting must actually suppress messages."""
import logging
import time
import pytest
from logsmith.rate_limit import RateLimitedLogger


class CapturingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def make_logger(name: str) -> tuple[logging.Logger, CapturingHandler]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = CapturingHandler()
    logger.addHandler(handler)
    return logger, handler


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

def test_first_call_always_passes_through():
    logger, handler = make_logger("rl.first_call")
    rl = RateLimitedLogger(logger, rate=1, per=60.0)
    rl.warning("first message")
    assert len(handler.records) == 1
    assert handler.records[0].getMessage() == "first message"


def test_rate_limit_suppresses_repeated_calls():
    """With rate=1/60s, only the first of many identical calls should log."""
    logger, handler = make_logger("rl.suppress")
    rl = RateLimitedLogger(logger, rate=1, per=60.0)
    for _ in range(10):
        rl.warning("hot path message")
    assert len(handler.records) == 1


def test_different_messages_tracked_independently():
    """Each unique message has its own quota."""
    logger, handler = make_logger("rl.independent")
    rl = RateLimitedLogger(logger, rate=1, per=60.0)
    rl.error("db connection failed")
    rl.error("cache miss")
    rl.error("db connection failed")  # should be suppressed
    rl.error("cache miss")             # should be suppressed
    assert len(handler.records) == 2
    messages = {r.getMessage() for r in handler.records}
    assert messages == {"db connection failed", "cache miss"}


def test_rate_higher_than_one_allows_multiple_calls():
    """rate=3 means 3 calls per window are allowed."""
    logger, handler = make_logger("rl.rate3")
    rl = RateLimitedLogger(logger, rate=3, per=60.0)
    for _ in range(5):
        rl.info("bursty info")
    assert len(handler.records) == 3


def test_all_log_level_methods_work():
    """warning, error, and info all go through the same gate."""
    logger, handler = make_logger("rl.levels")
    rl = RateLimitedLogger(logger, rate=1, per=60.0)
    rl.warning("w")
    rl.error("e")
    rl.info("i")
    assert len(handler.records) == 3


def test_window_resets_after_time_passes(monkeypatch):
    """After the time window expires the message is allowed again."""
    now = [0.0]
    monkeypatch.setattr(time, "monotonic", lambda: now[0])

    logger, handler = make_logger("rl.reset")
    rl = RateLimitedLogger(logger, rate=1, per=1.0)

    rl.warning("recurring")          # allowed — count=1
    rl.warning("recurring")          # suppressed — window full
    assert len(handler.records) == 1

    now[0] = 2.0                     # advance past the 1-second window
    rl.warning("recurring")          # allowed again
    assert len(handler.records) == 2


# ---------------------------------------------------------------------------
# Edge-case tests
# ---------------------------------------------------------------------------

def test_rate_zero_blocks_all_messages():
    """rate=0 should suppress every message."""
    logger, handler = make_logger("rl.zero")
    rl = RateLimitedLogger(logger, rate=0, per=60.0)
    rl.warning("should be blocked")
    rl.error("also blocked")
    assert len(handler.records) == 0


def test_empty_message_is_valid_key():
    """An empty string message should be handled without error."""
    logger, handler = make_logger("rl.empty_msg")
    rl = RateLimitedLogger(logger, rate=1, per=60.0)
    rl.warning("")
    rl.warning("")
    assert len(handler.records) == 1


def test_very_short_window(monkeypatch):
    """A tiny window (0.001 s) means any monotonic advance opens the gate again."""
    now = [0.0]
    monkeypatch.setattr(time, "monotonic", lambda: now[0])

    logger, handler = make_logger("rl.tiny_window")
    rl = RateLimitedLogger(logger, rate=1, per=0.001)

    rl.info("tick")
    assert len(handler.records) == 1

    now[0] = 0.002
    rl.info("tick")
    assert len(handler.records) == 2
