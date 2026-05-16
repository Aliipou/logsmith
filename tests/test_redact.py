"""Tests for RedactionFilter — PII must be masked in log extra fields."""
import logging
import pytest
from logsmith.redact import RedactionFilter, REDACTED


def make_record(**extra) -> logging.LogRecord:
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="event", args=(), exc_info=None,
    )
    for key, value in extra.items():
        setattr(record, key, value)
    return record


def apply(record: logging.LogRecord) -> logging.LogRecord:
    RedactionFilter().filter(record)
    return record


# ---------------------------------------------------------------------------
# Happy-path: known PII patterns are masked
# ---------------------------------------------------------------------------

def test_email_is_redacted():
    record = apply(make_record(user_email="jane.doe@example.com"))
    assert record.user_email == REDACTED


def test_credit_card_is_redacted():
    record = apply(make_record(card="4111 1111 1111 1111"))
    assert record.card == REDACTED


def test_ssn_is_redacted():
    record = apply(make_record(ssn="123-45-6789"))
    assert record.ssn == REDACTED


def test_ipv4_is_redacted():
    record = apply(make_record(client_ip="192.168.1.42"))
    assert record.client_ip == REDACTED


def test_phone_is_redacted():
    # The phone regex matches the digit portion; the leading '+' prefix is not
    # captured by the pattern, so it remains in place before [REDACTED].
    record = apply(make_record(contact="1 800 555 1234"))
    assert record.contact == REDACTED


def test_phone_with_plus_prefix_digit_portion_redacted():
    """Leading '+' is outside the regex match — the digits are still redacted."""
    record = apply(make_record(contact="+1 800 555 1234"))
    assert REDACTED in record.contact
    assert "800 555 1234" not in record.contact


def test_multiple_pii_fields_all_redacted():
    record = apply(make_record(
        email="a@b.com",
        ssn="000-11-2222",
        ip="10.0.0.1",
    ))
    assert record.email == REDACTED
    assert record.ssn == REDACTED
    assert record.ip == REDACTED


def test_pii_embedded_in_longer_string():
    """PII inside a longer string should still be redacted."""
    record = apply(make_record(note="Contact admin@corp.io for details"))
    assert "admin@corp.io" not in record.note
    assert REDACTED in record.note


def test_filter_always_returns_true():
    """RedactionFilter must never drop records — it always returns True."""
    f = RedactionFilter()
    record = make_record(safe_field="hello")
    assert f.filter(record) is True


# ---------------------------------------------------------------------------
# Happy-path: safe fields pass through untouched
# ---------------------------------------------------------------------------

def test_clean_string_is_unchanged():
    record = apply(make_record(action="login", status="ok"))
    assert record.action == "login"
    assert record.status == "ok"


def test_non_string_values_are_unchanged():
    record = apply(make_record(count=42, ratio=0.75, flag=True, items=[1, 2, 3]))
    assert record.count == 42
    assert record.ratio == 0.75
    assert record.flag is True
    assert record.items == [1, 2, 3]


# ---------------------------------------------------------------------------
# Edge-case tests
# ---------------------------------------------------------------------------

def test_empty_string_extra_field():
    record = apply(make_record(payload=""))
    assert record.payload == ""


def test_none_value_extra_field():
    record = apply(make_record(token=None))
    assert record.token is None


def test_standard_record_fields_not_modified():
    """Core LogRecord attributes in _SKIP must not be touched."""
    record = make_record()
    original_msg = record.msg
    original_levelname = record.levelname
    apply(record)
    assert record.msg == original_msg
    assert record.levelname == original_levelname


def test_no_pii_record_passes_filter():
    f = RedactionFilter()
    record = make_record(user="alice", action="view_dashboard")
    result = f.filter(record)
    assert result is True
    assert record.user == "alice"


def test_multiple_emails_in_single_field():
    """All occurrences of PII in one field value are replaced."""
    record = apply(make_record(cc="a@b.com and c@d.org"))
    assert "a@b.com" not in record.cc
    assert "c@d.org" not in record.cc
    assert REDACTED in record.cc
