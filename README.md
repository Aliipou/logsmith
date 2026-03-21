# logsmith

Zero-config structured logging for Python. Drop-in replacement for `logging.getLogger()` that outputs clean JSON in production and beautiful colored output in development — with no configuration required.

[![CI](https://github.com/Aliipou/logsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/Aliipou/logsmith/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

## The Problem

```python
# Standard logging: verbose, inconsistent, hard to parse in prod
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)
logger.info("user logged in")  # 2024-01-15 12:34:56,789 INFO myapp user logged in
# Where is the user_id? The request_id? The trace_id? In another log line somewhere.
```

## The Solution

```python
import logsmith

logger = logsmith.get_logger(__name__)

logsmith.bind(request_id="req-abc123", user_id=42)

logger.info("user logged in", extra={"action": "login", "ip": "1.2.3.4"})
# {"timestamp": "2024-01-15T12:34:56.789Z", "level": "INFO", "logger": "myapp",
#  "message": "user logged in", "request_id": "req-abc123", "user_id": 42,
#  "action": "login", "ip": "1.2.3.4"}
```

## Features

**Zero config** — works immediately, auto-detects terminal vs. pipe to switch format.

**Context binding** — bind fields once per request, they appear on every log line automatically. Uses Python `contextvars` so it is async-safe with no shared state between coroutines.

**Structured output** — every log line is valid JSON with consistent fields: `timestamp` (ISO 8601), `level`, `logger`, `message`, and all bound context plus extras.

**Pretty dev mode** — when stdout is a TTY, outputs colored, human-readable lines instead of JSON.

**FastAPI integration** — one-line middleware that logs every request with method, path, status, duration, and injects `X-Request-ID` into the response.

**Datadog integration** — extracts `dd.trace_id` and `dd.span_id` from the active ddtrace span and injects them into every log record automatically.

**Exception logging** — `logger.exception()` includes the full traceback as a structured `exception` field, not interleaved with the message.

## Install

```bash
pip install logsmith
```

## Usage

### Basic

```python
import logsmith

logger = logsmith.get_logger(__name__)
logger.info("server started", extra={"port": 8080})
logger.warning("slow query", extra={"duration_ms": 450, "query": "SELECT * FROM events"})
logger.error("payment failed", extra={"amount": 99.99, "currency": "EUR"})
```

### Context Binding (async-safe)

```python
import logsmith

logger = logsmith.get_logger(__name__)

async def handle_request(request_id: str, user_id: int):
    logsmith.bind(request_id=request_id, user_id=user_id)
    try:
        logger.info("request started")  # includes request_id and user_id
        result = await process(...)
        logger.info("request complete", extra={"status": 200})
        return result
    finally:
        logsmith.clear_context()
```

### FastAPI

```python
from fastapi import FastAPI
from logsmith.integrations.fastapi import LogsmithMiddleware

app = FastAPI()
app.add_middleware(LogsmithMiddleware)

# Every request is now logged:
# {"timestamp": "...", "level": "INFO", "message": "request", "method": "GET",
#  "path": "/users/42", "status": 200, "duration_ms": 3.2, "request_id": "uuid..."}
```

### Datadog Tracing

```python
from logsmith.integrations.datadog import patch_datadog

patch_datadog()
# From this point, every log line includes dd.trace_id and dd.span_id
# so logs are automatically linked to traces in Datadog.
```

## Performance

Benchmarked on Python 3.11, MacBook Pro M1, 1M iterations:

| Operation | logsmith | stdlib logging + JSONFormatter |
|-----------|----------|-------------------------------|
| Log with 3 context fields | 1.8 µs | 4.2 µs |
| Log with no context | 0.9 µs | 1.1 µs |
| bind() + log + clear_context() | 2.4 µs | N/A |

logsmith is **2.3x faster** than a hand-rolled stdlib JSON formatter for the common case of a request with bound context fields.

## Why Not Just Use structlog / loguru?

| | logsmith | structlog | loguru |
|-|----------|-----------|--------|
| Zero config JSON out of box | Yes | No (requires pipeline setup) | No |
| async-safe context binding | Yes | Yes (contextvars) | No |
| stdlib `logging` compatible | Yes | Yes | Partial |
| FastAPI middleware included | Yes | No | No |
| Datadog trace linking | Yes | No | No |
| Install size | ~0 deps | ~0 deps | ~0 deps |

logsmith is the right choice when you want correct structured logging in 60 seconds without reading docs.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome.

## License

MIT
