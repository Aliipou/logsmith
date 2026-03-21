"""logsmith — zero-config structured logging for Python."""
from __future__ import annotations
import logging
import json
import os
import time
import contextvars
from typing import Any, Optional

_context: contextvars.ContextVar[dict] = contextvars.ContextVar("logsmith_context", default={})

LEVEL_MAP = {
    "DEBUG": logging.DEBUG, "INFO": logging.INFO,
    "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL,
}

_GLOBAL_FIELDS: dict[str, Any] = {
    k: v for k, v in {
        "environment": os.environ.get("LOGSMITH_ENVIRONMENT"),
        "service": os.environ.get("LOGSMITH_SERVICE"),
        "host": os.environ.get("HOSTNAME"),
    }.items() if v
}


class JSONFormatter(logging.Formatter):
    """Formats log records as newline-delimited JSON with all extra fields included."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.") + f"{record.msecs:03.0f}Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Merge: global fields < context fields < record extras
        payload.update(_GLOBAL_FIELDS)
        payload.update(_context.get({}))

        skip = {"name", "msg", "args", "levelname", "levelno", "pathname", "filename",
                "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
                "created", "msecs", "relativeCreated", "thread", "threadName",
                "processName", "process", "message", "taskName"}

        for key, value in record.__dict__.items():
            if key not in skip:
                payload[key] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


class PrettyFormatter(logging.Formatter):
    """Human-readable colored output for local development."""

    COLORS = {
        "DEBUG": "[36m", "INFO": "[32m",
        "WARNING": "[33m", "ERROR": "[31m", "CRITICAL": "[35m",
    }
    RESET = "[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        ts = self.formatTime(record, "%H:%M:%S")
        extras = {k: v for k, v in record.__dict__.items()
                  if k not in {"name", "msg", "args", "levelname", "levelno", "pathname",
                                "filename", "module", "exc_info", "exc_text", "stack_info",
                                "lineno", "funcName", "created", "msecs", "relativeCreated",
                                "thread", "threadName", "processName", "process", "taskName"}}
        extra_str = " ".join(f"{k}={v!r}" for k, v in extras.items()) if extras else ""
        msg = f"{color}{ts} {record.levelname:<8}{self.RESET} [{record.name}] {record.getMessage()}"
        if extra_str:
            msg += f" {extra_str}"
        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)
        return msg


def _make_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    pretty = os.environ.get("LOGSMITH_PRETTY", "false").lower() == "true"
    handler.setFormatter(PrettyFormatter() if pretty else JSONFormatter())
    return handler


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a logsmith-configured logger.

    This is a drop-in replacement for logging.getLogger(). The first call
    configures the handler; subsequent calls return the cached logger.

    Args:
        name: Logger name, typically __name__.
        level: Override log level (default: LOGSMITH_LEVEL env var or INFO).

    Returns:
        Configured Logger instance with JSON/pretty output.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(_make_handler())
        logger.propagate = False
    lvl_name = level or os.environ.get("LOGSMITH_LEVEL", "INFO")
    logger.setLevel(LEVEL_MAP.get(lvl_name.upper(), logging.INFO))
    return logger


def bind(**fields: Any) -> None:
    """Bind fields to all subsequent log calls in the current async context.

    Bound fields are merged into every log record until the context ends
    or unbind() is called.

    Example::

        bind(user_id=123, tenant="acme")
        logger.info("Processing")  # includes user_id and tenant
    """
    current = dict(_context.get({}))
    current.update(fields)
    _context.set(current)


def unbind(*keys: str) -> None:
    """Remove specific keys from the current context."""
    current = dict(_context.get({}))
    for key in keys:
        current.pop(key, None)
    _context.set(current)


def clear_context() -> None:
    """Remove all bound context fields."""
    _context.set({})
