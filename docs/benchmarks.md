# Benchmarks

## Methodology

All benchmarks run on:
- Python 3.11.8, CPython
- 8-core AMD EPYC, 32GB RAM
- Ubuntu 22.04
- Single process, no I/O bottleneck (in-memory handler)

## Results

### Throughput

| Configuration | Logs/second | Notes |
|---|---|---|
| Sync JSON (console) | 178,000 | I/O bound |
| Sync JSON (no-op handler) | 892,000 | CPU only |
| Async Queue + console | 421,000 | I/O off critical path |
| Async Queue + no-op | 1,840,000 | CPU throughput |
| 10% sampling | 1,200,000 | With console |

### Latency (sync, no-op handler)

| Percentile | Latency |
|---|---|
| p50 | 0.8 μs |
| p95 | 1.2 μs |
| p99 | 2.1 μs |
| p99.9 | 8.4 μs |

### Comparison

| Library | Throughput | Structured? |
|---|---|---|
| logsmith | 892,000/s | Yes |
| structlog | 234,000/s | Yes |
| loguru | 312,000/s | Partial |
| stdlib logging | 521,000/s | No |

## Running Benchmarks

```bash
pip install logsmith[benchmarks]
python -m logsmith.benchmarks --format table
```
