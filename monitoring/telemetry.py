from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import logging

class Telemetry:
    def __init__(self):
        # Set up tracing
        trace.set_tracer_provider(TracerProvider())
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
        )
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def track_application(self, job_id: str, status: str, details: dict):
        """Track job application status"""
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("job_application") as span:
            span.set_attribute("job_id", job_id)
            span.set_attribute("status", status)
            self.logger.info(
                f"Job application {job_id} - Status: {status}",
                extra=details
            )
