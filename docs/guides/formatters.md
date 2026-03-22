# Log Formatters

## JSON Formatter (Default)

```python
from logsmith.formatters import JsonFormatter
logger = logsmith.get_logger("app", formatter=JsonFormatter(indent=None))
```

Output:
```json
{"ts":"2024-01-15T10:23:45.123Z","level":"INFO","logger":"app","msg":"Started","port":8080}
```

## Pretty Formatter (Development)

```python
from logsmith.formatters import PrettyFormatter
logger = logsmith.get_logger("app", formatter=PrettyFormatter(colors=True))
```

Output:
```
2024-01-15 10:23:45 INFO  app │ Started port=8080
```

## Logfmt Formatter

```python
from logsmith.formatters import LogfmtFormatter
logger = logsmith.get_logger("app", formatter=LogfmtFormatter())
```

Output:
```
ts=2024-01-15T10:23:45Z level=INFO logger=app msg=Started port=8080
```

## Custom Formatter

```python
from logsmith.formatters import BaseFormatter, LogEntry

class MyFormatter(BaseFormatter):
    def format(self, entry: LogEntry) -> str:
        return f"[{entry.level}] {entry.message}"
```
