# Multi-Output Configuration

```python
logger = logsmith.get_logger('app', handlers=[
    ConsoleHandler(format='pretty', min_level='DEBUG'),
    FileHandler('errors.log', min_level='WARNING'),
    SlackHandler(webhook_url=settings.slack_webhook, min_level='CRITICAL'),
])
```
