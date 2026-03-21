"""FastAPI middleware for automatic request/response logging."""
from __future__ import annotations
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logsmith import get_logger, bind, clear_context

logger = get_logger("logsmith.access")


class LogsmithMiddleware(BaseHTTPMiddleware):
    """Logs every request with method, path, status, duration, and request ID.

    Injects request_id into log context so all logs within a request
    are automatically correlated.

    Usage::

        from logsmith.integrations.fastapi import LogsmithMiddleware
        app.add_middleware(LogsmithMiddleware)
    """

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
        bind(request_id=request_id)
        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "request",
                method=request.method,
                path=request.url.path,
                status=status_code,
                duration_ms=duration_ms,
                client=request.client.host if request.client else "unknown",
            )
            clear_context()
