"""Sentry integration for logsmith.

Automatically captures ERROR and CRITICAL log records to Sentry,
including all bound context fields as extra data.
"""
from __future__ import annotations
import logging
from typing import Any


class SentryHandler(logging.Handler):
    """Logging handler that sends ERROR+ records to Sentry.

    Usage::

        import sentry_sdk
        from logsmith.integrations.sentry import SentryHandler

        sentry_sdk.init(dsn="https://...")
        logging.getLogger().addHandler(SentryHandler())
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            import sentry_sdk
        except ImportError:
            return

        level_map = {
            logging.WARNING: "warning",
            logging.ERROR: "error",
            logging.CRITICAL: "fatal",
        }
        sentry_level = level_map.get(record.levelno, "info")

        extra: dict[str, Any] = {}
        for key in vars(record):
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
            }:
                extra[key] = getattr(record, key)

        with sentry_sdk.new_scope() as scope:
            scope.set_level(sentry_level)
            for key, value in extra.items():
                scope.set_extra(key, value)

            if record.exc_info:
                sentry_sdk.capture_exception(record.exc_info[1])
            else:
                sentry_sdk.capture_message(record.getMessage(), level=sentry_level)
