# Log Sampling Guide

## Why Sample?

High-volume services generate millions of log entries. Sampling reduces storage costs while preserving signal.

## Usage

```python
import logsmith

# Sample 10% of debug logs, 100% of warnings+
logger = logsmith.get_logger("high-volume", sample_rate=0.1, sample_min_level="WARNING")
```

## Adaptive Sampling

```python
from logsmith.sampling import AdaptiveSampler

sampler = AdaptiveSampler(
    target_rps=1000,      # target log records per second
    window_seconds=60,    # measurement window
)
logger = logsmith.get_logger("api", sampler=sampler)
```
