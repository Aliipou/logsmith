# Metrics Integration

Emit log-based metrics to Prometheus:

```python
from logsmith.metrics import LogMetricsMiddleware
logger = logsmith.get_logger('api', middlewares=[LogMetricsMiddleware(counter_name='log_entries_total', labels=['level', 'service'])])
```
