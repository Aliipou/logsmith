"""Tests for logsmith core functionality."""
import json
import logging
import pytest
from logsmith import get_logger, bind, unbind, clear_context, JSONFormatter


def capture_json_log(logger_name: str, level: str, msg: str, **kwargs) -> dict:
    """Helper: capture what JSONFormatter produces for a log call."""
    records = []

    class CapturingHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    log = logging.getLogger(logger_name)
    handler = CapturingHandler()
    handler.setFormatter(JSONFormatter())
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    try:
        getattr(log, level.lower())(msg, **kwargs)
    finally:
        log.removeHandler(handler)

    assert records, "No log record captured"
    return json.loads(handler.format(records[0]))


def test_json_output_has_required_fields():
    payload = capture_json_log("test.basic", "info", "Hello")
    assert "timestamp" in payload
    assert payload["level"] == "INFO"
    assert payload["logger"] == "test.basic"
    assert payload["message"] == "Hello"


def test_extra_fields_appear_in_json():
    payload = capture_json_log("test.extra", "info", "Event", user_id=42, action="login")
    assert payload["user_id"] == 42
    assert payload["action"] == "login"


def test_bind_adds_fields_to_context():
    clear_context()
    bind(tenant="acme", request_id="abc123")
    payload = capture_json_log("test.bind", "info", "Context test")
    assert payload["tenant"] == "acme"
    assert payload["request_id"] == "abc123"
    clear_context()


def test_unbind_removes_specific_fields():
    clear_context()
    bind(a=1, b=2)
    unbind("a")
    payload = capture_json_log("test.unbind", "info", "After unbind")
    assert "a" not in payload
    assert payload["b"] == 2
    clear_context()


def test_clear_context_removes_all():
    bind(x=1, y=2)
    clear_context()
    payload = capture_json_log("test.clear", "info", "After clear")
    assert "x" not in payload
    assert "y" not in payload


def test_get_logger_returns_logger():
    log = get_logger("test.module")
    assert isinstance(log, logging.Logger)
    assert log.name == "test.module"


def test_exception_info_in_json():
    records = []

    class CapturingHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    log = logging.getLogger("test.exc")
    h = CapturingHandler()
    h.setFormatter(JSONFormatter())
    log.addHandler(h)
    try:
        raise ValueError("test error")
    except ValueError:
        log.exception("Something failed")
    log.removeHandler(h)

    payload = json.loads(h.format(records[0]))
    assert "exception" in payload
    assert "ValueError" in payload["exception"]
