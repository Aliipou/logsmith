# Cloud Provider Guides

## Google Cloud Logging

```python
from logsmith.handlers import CloudLoggingHandler
import google.cloud.logging

client = google.cloud.logging.Client()
logger = logsmith.get_logger("app", handlers=[CloudLoggingHandler(client)])
```

## AWS CloudWatch

```python
from logsmith.handlers import CloudWatchHandler

logger = logsmith.get_logger("app", handlers=[
    CloudWatchHandler(
        log_group="/my-app/production",
        log_stream="api",
        region="eu-west-1",
    )
])
```

## Azure Monitor

```python
from logsmith.handlers import AzureMonitorHandler

logger = logsmith.get_logger("app", handlers=[
    AzureMonitorHandler(connection_string=settings.azure_monitor_connection_string)
])
```
