# Structured Context Guide

## Adding Context to Log Entries

logsmith supports structured context via `bind()`:

```python
import logsmith

logger = logsmith.get_logger("my-app")
request_logger = logger.bind(request_id="abc123", user_id=42)

request_logger.info("Processing request", endpoint="/api/users")
# Output: {"level":"INFO","msg":"Processing request","request_id":"abc123","user_id":42,"endpoint":"/api/users"}
```

## Thread-Local Context

```python
from logsmith import context

with context.bind(trace_id="t-001"):
    logger.info("Inside trace")  # automatically includes trace_id
```
