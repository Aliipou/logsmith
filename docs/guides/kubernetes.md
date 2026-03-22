# Kubernetes Deployment Guide

## ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logsmith-config
data:
  LOGSMITH_LEVEL: "INFO"
  LOGSMITH_FORMAT: "json"
  LOGSMITH_SAMPLE_RATE: "1.0"
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: api
        image: my-app:latest
        envFrom:
        - configMapRef:
            name: logsmith-config
```

## Log Aggregation

logsmith JSON output integrates with:

**Loki + Grafana:**
```yaml
# promtail/config.yml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - json:
          expressions:
            level: level
            msg: msg
            trace_id: trace_id
```

**Elastic APM:**
```python
from logsmith.integrations import ElasticAPMHandler
logger = logsmith.get_logger("app", handlers=[ElasticAPMHandler()])
```
