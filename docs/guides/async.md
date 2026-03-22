# Async Logging

## AsyncHandler

Wrap any handler to make it non-blocking:

```python
from logsmith.handlers import AsyncHandler, FileHandler

# Logs are queued in memory and written in background thread
async_handler = AsyncHandler(
    FileHandler("app.log"),
    queue_size=50000,
    overflow="drop",  # or "block" or "sample"
)
logger = logsmith.get_logger("app", handlers=[async_handler])
```

## FastAPI Integration

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logsmith

@asynccontextmanager
async def lifespan(app: FastAPI):
    logsmith.configure(handlers=[AsyncHandler(ConsoleHandler())])
    yield
    await logsmith.flush()  # flush on shutdown

app = FastAPI(lifespan=lifespan)
```

## Structured Async Context

```python
import asyncio
import logsmith

async def handle_request(request_id: str):
    async with logsmith.async_context(request_id=request_id):
        await do_work()
        # All logs inside include request_id automatically
```
