# Error Context

Automatic exception capture:

```python
try:
    process_order(order)
except Exception as e:
    logger.exception('Order processing failed', order_id=order.id)
```
