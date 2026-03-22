# FAQ

## Is logsmith thread-safe?
Yes, all built-in handlers are thread-safe.

## Does it work with async Python?
Yes. Use `AsyncHandler` for non-blocking I/O.

## How do I suppress logs in tests?
```python
logsmith.configure(min_level='CRITICAL')
```
