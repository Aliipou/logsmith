# JSON Output Format

logsmith emits structured JSON by default.

## Output Schema

```json
{
  "timestamp": "2024-01-15T10:23:45.123456Z",
  "level": "INFO",
  "logger": "my-app",
  "message": "User authenticated",
  "user_id": 42,
  "duration_ms": 12.3,
  "trace_id": "abc123"
}
```

## Configuration

```python
import logsmith

# Default: JSON to stdout
logger = logsmith.get_logger("app")

# Pretty-print for development
logger = logsmith.get_logger("app", format="pretty")

# Custom timestamp format
logger = logsmith.get_logger("app", timestamp_format="epoch_ms")
```
