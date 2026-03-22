# PII Redaction

Protect sensitive data before it reaches your logs.

## Automatic Redaction

```python
import logsmith

logger = logsmith.get_logger("app", redact_fields=["password", "token", "secret", "credit_card"])

logger.info("User login", user={"email": "user@example.com", "password": "secret123"})
# Output: {"msg":"User login","user":{"email":"user@example.com","password":"[REDACTED]"}}
```

## Pattern-Based Redaction

```python
from logsmith.redaction import PatternRedactor

redactor = PatternRedactor(patterns=[
    r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # credit card
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email
])
logger = logsmith.get_logger("app", redactor=redactor)
```

## Custom Redactor

```python
from logsmith.redaction import BaseRedactor

class MyRedactor(BaseRedactor):
    def redact(self, key: str, value: object) -> object:
        if "ssn" in key.lower():
            return "***-**-" + str(value)[-4:]
        return value
```
