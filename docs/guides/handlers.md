# Log Handlers

## Available Handlers

### ConsoleHandler (Default)
Writes JSON to stdout.

```python
from logsmith.handlers import ConsoleHandler
logger = logsmith.get_logger("app", handlers=[ConsoleHandler(format="json")])
```

### FileHandler
Writes to a rotating file.

```python
from logsmith.handlers import FileHandler
logger = logsmith.get_logger("app", handlers=[
    FileHandler("app.log", max_size="100MB", max_files=10)
])
```

### AsyncHandler
Non-blocking handler for high-throughput services.

```python
from logsmith.handlers import AsyncHandler
logger = logsmith.get_logger("app", handlers=[
    AsyncHandler(ConsoleHandler(), queue_size=10000)
])
```

## Multiple Handlers

```python
logger = logsmith.get_logger("app", handlers=[
    ConsoleHandler(),
    FileHandler("errors.log", min_level="ERROR"),
])
```
