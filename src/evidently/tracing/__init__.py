import os
import urllib.parse
from functools import wraps
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_TRACE_COLLECTOR_ADDRESS = os.getenv("EVIDENTLY_TRACE_COLLECTOR", "https://app.evidently.cloud")
_TRACE_COLLECTOR_TYPE = os.getenv("EVIDENTLY_TRACE_COLLECTOR_TYPE", "http")
_TRACE_COLLECTOR_API_KEY = os.getenv("EVIDENTLY_TRACE_COLLECTOR_API_KEY", "")


_tracer: Optional[trace.TracerProvider] = None


def trace_event(track_args: Optional[List[str]] = None, ignore_args: Optional[List[str]] = None):
    """
    Trace given function call.

    Args:
        track_args: list of arguments to capture, if set to None - capture all arguments (default),
                    if set to [] do not capture any arguments
        ignore_args: list of arguments to ignore, if set to None - do not ignore any arguments.
    """

    def wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def func(*args, **kwargs):
            import inspect

            if _tracer is None:
                raise ValueError("TracerProvider not initialized, use init_tracer() or register_span_processor")

            sign = inspect.signature(f)
            bind = sign.bind(*args, **kwargs)
            with _tracer.start_as_current_span(f"{f.__name__}") as span:
                final_args = track_args
                if track_args is None:
                    final_args = list(sign.parameters.keys())
                if ignore_args is not None:
                    final_args = [item for item in final_args if item not in ignore_args]
                for tracked in final_args:
                    span.set_attribute(tracked, bind.arguments[tracked])
                result = f(*args, **kwargs)
                span.set_attribute("result", result)
            return result

        return func

    return wrapper


def register_span_processor(
    tracer_provider: TracerProvider,
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
) -> None:
    """
    Register Evidently telemetry tracing span processor in existing tracer provider.
    Args:
        tracer_provider: provider to register tracing in
        address: address of collector service
        exporter_type: type of exporter to use "grpc" or "http"
        api_key: authorization api key for Evidently tracing
    """
    global _tracer  # noqa: PLW0603

    _address = address or _TRACE_COLLECTOR_ADDRESS
    _exporter_type = exporter_type or _TRACE_COLLECTOR_TYPE
    _api_key = api_key or _TRACE_COLLECTOR_API_KEY
    exporter = None
    if _exporter_type == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        exporter = OTLPSpanExporter(_address, headers=[] if _api_key is None else [("authorization", _api_key)])
    elif _exporter_type == "http":
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        exporter = OTLPSpanExporter(
            urllib.parse.urljoin(_address, "/v1/traces"),
            headers=dict([] if _api_key is None else [("authorization", _api_key)]),
        )

    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    _tracer = tracer_provider.get_tracer("evidently")


def init_tracing(
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
    *,
    as_global: bool = True,
) -> None:
    """
    Initialize Evidently tracing
    Args:
        address: address of collector service
        exporter_type: type of exporter to use "grpc" or "http"
        api_key: authorization api key for Evidently tracing
        as_global: indicated when to register provider globally for opentelemetry of use local one
                   Can be useful when you don't want to mix already existing OpenTelemetry tracing with Evidently one,
                   but may require additional configuration
    """
    global _tracer  # noqa: PLW0603

    _provider = TracerProvider()
    register_span_processor(_provider, address, exporter_type, api_key)

    if as_global:
        trace.set_tracer_provider(_provider)
        _tracer = trace.get_tracer("evidently")
    else:
        _tracer = _provider.get_tracer("evidently")
