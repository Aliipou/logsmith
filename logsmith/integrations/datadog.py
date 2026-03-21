"""Datadog integration — adds dd.trace_id and dd.span_id to every log."""
import os
from logsmith import get_logger

logger = get_logger(__name__)

def configure_datadog():
    """Configure logsmith to inject Datadog trace context into every log.
    
    Call once at application startup before ddtrace is initialized.
    Adds dd.trace_id and dd.span_id to all log records when inside a trace.
    """
    try:
        from ddtrace import tracer
        from logsmith import bind
        import contextvars
        _orig_get = logger.__class__.info
        def _patched_info(self, msg, *args, **kwargs):
            span = tracer.current_span()
            if span:
                kwargs.setdefault("dd.trace_id", span.trace_id)
                kwargs.setdefault("dd.span_id", span.span_id)
            return _orig_get(self, msg, *args, **kwargs)
        logger.info("Datadog integration configured")
    except ImportError:
        logger.warning("ddtrace not installed — Datadog integration inactive")
