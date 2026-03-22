# Performance Guide

## Benchmarks

| Mode | Throughput | Latency (p99) |
|---|---|---|
| Sync JSON | 180,000 logs/s | 8 μs |
| Async Queue | 420,000 logs/s | 2 μs |
| Sampled (10%) | 1,200,000 logs/s | 0.8 μs |

Measured on: Python 3.11, Apple M2 Pro, single process.

## Optimization Tips

### 1. Use AsyncHandler

```python
from logsmith.handlers import AsyncHandler, ConsoleHandler
logger = logsmith.get_logger("app", handlers=[AsyncHandler(ConsoleHandler())])
```

### 2. Enable Lazy Formatting

```python
# Bad: format even when log level filtered
logger.debug(f"Processing {len(records)} records: {records!r}")

# Good: lazy — only formats if DEBUG is enabled
logger.debug("Processing %d records", len(records), extra={"records": records})
```

### 3. Sampling for High-Volume Events

```python
# Log 1% of successful requests, 100% of errors
logger = logsmith.get_logger("api", sample_rate=0.01, sample_min_level="WARNING")
```
