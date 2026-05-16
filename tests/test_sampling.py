"""Tests for SamplingFilter — probabilistic log dropping."""
import logging
import random
import pytest
from logsmith.sampling import SamplingFilter


def make_record(level: int = logging.DEBUG, msg: str = "test") -> logging.LogRecord:
    return logging.LogRecord(
        name="test", level=level, pathname="", lineno=0,
        msg=msg, args=(), exc_info=None,
    )


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

def test_rate_1_passes_all_records():
    """rate=1.0 should never drop anything regardless of level."""
    f = SamplingFilter(rate=1.0, min_level=logging.WARNING)
    for _ in range(50):
        assert f.filter(make_record(logging.DEBUG)) is True


def test_records_at_or_above_min_level_always_pass():
    """WARNING+ must always pass through even when rate is very low."""
    f = SamplingFilter(rate=0.0, min_level=logging.WARNING)
    assert f.filter(make_record(logging.WARNING)) is True
    assert f.filter(make_record(logging.ERROR)) is True
    assert f.filter(make_record(logging.CRITICAL)) is True


def test_rate_0_drops_all_below_min_level():
    """rate=0.0 should drop every sub-threshold record."""
    f = SamplingFilter(rate=0.0, min_level=logging.WARNING)
    for _ in range(50):
        assert f.filter(make_record(logging.DEBUG)) is False
        assert f.filter(make_record(logging.INFO)) is False


def test_sampling_is_probabilistic(monkeypatch):
    """With rate=0.5, roughly half of below-threshold records pass."""
    # Alternate random() between 0.3 (pass) and 0.7 (drop)
    values = iter([0.3, 0.7] * 50)
    monkeypatch.setattr(random, "random", lambda: next(values))

    f = SamplingFilter(rate=0.5, min_level=logging.WARNING)
    results = [f.filter(make_record(logging.DEBUG)) for _ in range(100)]
    passed = sum(results)
    assert passed == 50  # exactly half given the deterministic mock


def test_info_level_record_sampled():
    """INFO is below default WARNING min_level, so it goes through sampling."""
    f = SamplingFilter(rate=1.0, min_level=logging.WARNING)
    assert f.filter(make_record(logging.INFO)) is True


# ---------------------------------------------------------------------------
# Edge-case tests
# ---------------------------------------------------------------------------

def test_invalid_rate_raises_value_error():
    with pytest.raises(ValueError, match="rate must be in"):
        SamplingFilter(rate=1.5)

    with pytest.raises(ValueError, match="rate must be in"):
        SamplingFilter(rate=-0.1)


def test_rate_exactly_zero_and_one_are_valid():
    """Boundary values 0.0 and 1.0 must not raise."""
    SamplingFilter(rate=0.0)
    SamplingFilter(rate=1.0)


def test_min_level_debug_means_everything_bypasses_sampling():
    """When min_level=DEBUG, all records pass via the level gate, never sampling."""
    f = SamplingFilter(rate=0.0, min_level=logging.DEBUG)
    assert f.filter(make_record(logging.DEBUG)) is True
    assert f.filter(make_record(logging.INFO)) is True


def test_default_rate_is_1():
    """Default constructor should pass all records."""
    f = SamplingFilter()
    assert f.filter(make_record(logging.DEBUG)) is True


def test_filter_does_not_mutate_record():
    """Applying the filter must not modify the log record."""
    f = SamplingFilter(rate=1.0, min_level=logging.WARNING)
    record = make_record(logging.DEBUG, msg="original")
    f.filter(record)
    assert record.getMessage() == "original"
