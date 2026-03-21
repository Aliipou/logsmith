"""Tests for JSON and Pretty formatters."""
import json
import logging
from logsmith import JSONFormatter, PrettyFormatter


def make_record(msg: str, level: int = logging.INFO, **extra) -> logging.LogRecord:
    record = logging.LogRecord(
        name="test", level=level, pathname="", lineno=0,
        msg=msg, args=(), exc_info=None
    )
    for k, v in extra.items():
        setattr(record, k, v)
    return record


def test_json_formatter_valid_json():
    fmt = JSONFormatter()
    record = make_record("test message")
    output = fmt.format(record)
    parsed = json.loads(output)
    assert parsed["message"] == "test message"


def test_json_formatter_extra_fields():
    fmt = JSONFormatter()
    record = make_record("msg", user_id=99)
    output = fmt.format(record)
    parsed = json.loads(output)
    assert parsed["user_id"] == 99


def test_pretty_formatter_returns_string():
    fmt = PrettyFormatter()
    record = make_record("pretty test")
    output = fmt.format(record)
    assert isinstance(output, str)
    assert "pretty test" in output


def test_json_formatter_handles_non_serializable():
    fmt = JSONFormatter()
    record = make_record("msg", obj=object())
    output = fmt.format(record)  # should not raise
    assert json.loads(output)
