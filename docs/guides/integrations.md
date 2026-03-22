# Integrations

## Standard Library Logging

logsmith captures Python standard library logs:

```python
import logsmith
import logging

logsmith.capture_stdlib(level="WARNING")  # capture all stdlib WARNING+ logs

# Now this goes through logsmith
logging.getLogger("uvicorn").warning("Worker timeout")
# Output: {"level":"WARNING","logger":"uvicorn","msg":"Worker timeout",...}
```

## Sentry Integration

```python
from logsmith.integrations import SentryHandler
import sentry_sdk

sentry_sdk.init(dsn="...")
logger = logsmith.get_logger("app", handlers=[SentryHandler(min_level="ERROR")])
```

## Datadog Integration

```python
from logsmith.integrations import DatadogHandler

logger = logsmith.get_logger("app", handlers=[
    DatadogHandler(api_key="...", service="my-api", env="prod")
])
```

## OpenTelemetry Trace Correlation

```python
from logsmith.integrations import OtelTraceMiddleware

logger = logsmith.get_logger("app")
logger.add_middleware(OtelTraceMiddleware())
# Automatically adds trace_id and span_id to every log entry
```
