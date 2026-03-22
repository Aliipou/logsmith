# Log Filters

Filters allow you to suppress or transform log entries before they reach handlers.

## Level Filter

```python
import logsmith

# Only log WARNING and above in production
logger = logsmith.get_logger("app")
logger.set_min_level("WARNING" if is_production else "DEBUG")
```

## Custom Filter

```python
from logsmith.filters import BaseFilter, LogEntry

class HealthCheckFilter(BaseFilter):
    def should_log(self, entry: LogEntry) -> bool:
        # Suppress noisy health check logs
        return not (entry.path == "/health" and entry.status_code == 200)

logger = logsmith.get_logger("api", filters=[HealthCheckFilter()])
```

## Rate Limiter Filter

```python
from logsmith.filters import RateLimiterFilter

# Max 100 identical messages per minute
filter = RateLimiterFilter(rate=100, window_seconds=60, key_fn=lambda e: e.message)
logger = logsmith.get_logger("app", filters=[filter])
```
