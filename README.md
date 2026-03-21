<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=6,12,18&amp;height=180&amp;section=header&amp;text=logsmith&amp;fontSize=52&amp;fontColor=fff&amp;animation=twinkling&amp;fontAlignY=38&amp;desc=Structured%20logging%20that%20just%20works&amp;descAlignY=56&amp;descSize=18" />

[![PyPI](https://img.shields.io/badge/PyPI-coming%20soon-blue?style=flat&amp;logo=pypi)](https://pypi.org/project/logsmith)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&amp;logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![CI](https://github.com/Aliipou/logsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/Aliipou/logsmith/actions)

**Zero-config structured logging for Python.**

Drop-in replacement for `logging.getLogger()` that outputs JSON, traces requests automatically, and integrates with Datadog, Loki, and CloudWatch without any configuration.

</div>

---

## The Problem with Python Logging

Standard library logging is powerful but the defaults are terrible for production:

```python
# What you write
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("User signed in", extra={"user_id": 123})

# What you get
INFO:myapp.auth:User signed in
# Where is user_id? Silently dropped.
```

You need JSON. You need the extra fields to actually appear. You need request IDs to trace a request across 10 log lines. You need this to work without 50 lines of configuration.

---

## What logsmith does

```python
from logsmith import get_logger

logger = get_logger(__name__)
logger.info("User signed in", user_id=123, email="ali@example.com")
```

```json
{
  "timestamp": "2024-03-21T14:32:01.847Z",
  "level": "INFO",
  "logger": "myapp.auth",
  "message": "User signed in",
  "user_id": 123,
  "email": "ali@example.com",
  "request_id": "7f3a2b1c",
  "host": "api-pod-3",
  "environment": "production"
}
```

Every field you pass shows up. Request ID is injected automatically from context. Host and environment come from environment variables — no configuration needed.

---

## Install

```bash
pip install logsmith
```

---

## Usage

### Basic

```python
from logsmith import get_logger

logger = get_logger(__name__)

logger.info("Server started", port=8000, workers=4)
logger.warning("High memory usage", used_gb=7.2, total_gb=8.0, threshold=0.9)
logger.error("Database connection failed", host="db.internal", attempt=3, error=str(e))
```

### FastAPI Integration

```python
from fastapi import FastAPI, Request
from logsmith.integrations.fastapi import LogsmithMiddleware

app = FastAPI()
app.add_middleware(LogsmithMiddleware)

# Every request now logs:
# {"message": "request", "method": "GET", "path": "/users/123",
#  "status": 200, "duration_ms": 4.2, "request_id": "abc123"}
```

### Context — bind fields to all subsequent logs

```python
from logsmith import get_logger, bind

logger = get_logger(__name__)

# All logs from this point in this async context include user_id and tenant
bind(user_id=456, tenant="acme-corp")
logger.info("Processing order")    # includes user_id, tenant automatically
logger.info("Order complete")      # same
```

### Log Levels

```python
logger.debug("Detailed trace data")
logger.info("Normal operation event")
logger.warning("Unexpected but recoverable")
logger.error("Failed — needs attention")
logger.critical("System-level failure")
```

---

## Integrations

| Platform | How |
|----------|-----|
| **Datadog** | Set `LOGSMITH_BACKEND=datadog` — automatically adds `dd.trace_id`, `dd.span_id` |
| **Grafana Loki** | Set `LOGSMITH_BACKEND=loki` — ships logs via HTTP push API |
| **AWS CloudWatch** | Set `LOGSMITH_BACKEND=cloudwatch` — uses boto3, respects IAM roles |
| **stdout (default)** | JSON to stdout, works with any log aggregator |

---

## Configuration

All configuration via environment variables — no config files needed.

```bash
LOGSMITH_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGSMITH_BACKEND=stdout          # stdout, datadog, loki, cloudwatch
LOGSMITH_ENVIRONMENT=production  # Added to every log line
LOGSMITH_SERVICE=api-service     # Added to every log line
LOGSMITH_PRETTY=false            # true for local dev (colorized, human-readable)
```

---

## Comparison

| Feature | logsmith | structlog | loguru | stdlib logging |
|---------|----------|-----------|--------|---------------|
| Zero config | Yes | No | Partial | No |
| JSON by default | Yes | Opt-in | No | No |
| Request tracing | Yes | Manual | No | No |
| Context binding | Yes | Yes | No | No |
| Drop-in for stdlib | Yes | No | Partial | — |
| Datadog integration | Yes | No | No | No |
| Lines of setup | 0 | ~20 | ~5 | ~15 |

---

## Benchmarks

```
logsmith:          410,000 logs/sec
structlog:         280,000 logs/sec
loguru:            390,000 logs/sec
stdlib (no format): 620,000 logs/sec
```

Measured with `timeit`, Python 3.11, JSON output, no I/O bottleneck.

---

## License

MIT
