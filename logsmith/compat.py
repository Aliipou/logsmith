"""Compatibility shim for migrating from stdlib logging to logsmith.

Drop-in replacements for common stdlib logging patterns.
"""
from __future__ import annotations
import logging
import logsmith


def getLogger(name: str) -> logging.Logger:
    """Drop-in replacement for logging.getLogger() that returns a logsmith-configured logger."""
    return logsmith.get_logger(name)


class CompatHandler(logging.Handler):
    """Handler that routes stdlib logging records through logsmith formatters."""

    def emit(self, record: logging.LogRecord) -> None:
        logger = logsmith.get_logger(record.name)
        method = getattr(logger, record.levelname.lower(), logger.info)
        method(record.getMessage())
