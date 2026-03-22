# Distributed Tracing Correlation

## OpenTelemetry

```python
from logsmith.integrations import OtelTraceMiddleware
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Set up tracer
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

# Correlate logs with traces
logger = logsmith.get_logger("app")
logger.add_middleware(OtelTraceMiddleware())  # adds trace_id, span_id to all logs
```

## Jaeger

```python
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
```

## Zipkin

```python
from opentelemetry.exporter.zipkin.json import ZipkinExporter

exporter = ZipkinExporter(endpoint="http://zipkin:9411/api/v2/spans")
```

Every log entry with active tracing will include:
```json
{"trace_id": "abc123...", "span_id": "def456...", "trace_flags": "01"}
```
