# Testing with logsmith

## Capturing Logs in Tests

```python
import pytest
from logsmith.testing import LogCapture

def test_warning_on_retry(app):
    with LogCapture() as logs:
        app.process_with_retry(failing_input)

    warning = logs.find(level="WARNING", message_contains="retry")
    assert warning is not None
    assert warning["attempt"] == 2
```

## Asserting Log Structure

```python
from logsmith.testing import LogCapture

def test_structured_output():
    with LogCapture() as logs:
        logger.info("Order processed", order_id="ord-001", amount=99.99)

    entry = logs.find(message="Order processed")
    assert entry["order_id"] == "ord-001"
    assert entry["amount"] == 99.99
    assert entry["level"] == "INFO"
```

## pytest Fixture

```python
# conftest.py
import pytest
from logsmith.testing import LogCapture

@pytest.fixture
def log_capture():
    with LogCapture() as logs:
        yield logs
```
