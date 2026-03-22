"""Async context manager for scoped log context binding."""
from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logsmith


@asynccontextmanager
async def log_context(**fields) -> AsyncGenerator[None, None]:
    """Async context manager that binds fields for the duration of a block.

    Usage::

        async with log_context(request_id="abc", user_id=42):
            logger.info("processing request")
            await do_work()
        # Fields are cleared after the block
    """
    logsmith.bind(**fields)
    try:
        yield
    finally:
        logsmith.unbind(*fields.keys())
