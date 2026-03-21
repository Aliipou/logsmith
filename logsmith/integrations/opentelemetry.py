"""OpenTelemetry integration for logsmith.

Automatically injects trace_id, span_id, and trace_flags from the
active OpenTelemetry span into every log record.
"""
from __future__ import annotations
import logging
from typing import Any


def _get_otel_context() -> dict[str, Any]:
    """Extract trace context from the active OpenTelemetry span."""
    try:
        from opentelemetry import trace
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.is_valid:
            return {
                "trace_id": format(ctx.trace_id, "032x"),
                "span_id": format(ctx.span_id, "016x"),
                "trace_flags": ctx.trace_flags,
            }
    except ImportError:
        pass
    return {}


class OTelInjectingFilter(logging.Filter):
    """Logging filter that injects OpenTelemetry context into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in _get_otel_context().items():
            setattr(record, key, value)
        return True


def patch_opentelemetry() -> None:
    """Patch the root logger to inject OTel context into all log records.

    Call once at application startup, before any loggers are created::

        from logsmith.integrations.opentelemetry import patch_opentelemetry
        patch_opentelemetry()
    """
    logging.getLogger().addFilter(OTelInjectingFilter())
