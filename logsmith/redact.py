"""PII redaction filter for GDPR-compliant structured logging."""
from __future__ import annotations
import logging
import re
from typing import Any


_PATTERNS: dict[str, re.Pattern] = {
    "email": re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"),
    "credit_card": re.compile(r"\b(?:\d[ \-]?){13,16}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b(?:\+?\d[\s\-]?){8,15}\b"),
    "ip_v4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}

REDACTED = "[REDACTED]"


def _redact_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    for pattern in _PATTERNS.values():
        value = pattern.sub(REDACTED, value)
    return value


class RedactionFilter(logging.Filter):
    """Logging filter that redacts PII from log record extra fields.

    Scans all string-valued attributes on the log record and replaces
    email addresses, credit card numbers, SSNs, phone numbers, and
    IPv4 addresses with "[REDACTED]".

    Usage::

        logging.getLogger().addFilter(RedactionFilter())
    """

    _SKIP = frozenset({
        "name", "msg", "args", "levelname", "levelno", "pathname",
        "filename", "module", "exc_info", "exc_text", "stack_info",
        "lineno", "funcName", "created", "msecs", "relativeCreated",
        "thread", "threadName", "processName", "process",
    })

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in vars(record).items():
            if key not in self._SKIP:
                setattr(record, key, _redact_value(value))
        return True
