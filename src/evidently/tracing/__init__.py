import os
import urllib.parse
from functools import wraps
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_TRACE_COLLECTOR_ADDRESS = os.getenv("EVIDENTLY_TRACE_COLLECTOR", "https://app.evidently.cloud")
_TRACE_COLLECTOR_TYPE = os.getenv("EVIDENTLY_TRACE_COLLECTOR_TYPE", "http")
_TRACE_COLLECTOR_API_KEY = os.getenv("EVIDENTLY_TRACE_COLLECTOR_API_KEY", "")
_TRACE_COLLECTOR_EXPORT_ID = os.getenv("EVIDENTLY_TRACE_COLLECTOR_EXPORT_ID", "")
_TRACE_COLLECTOR_TEAM_ID = os.getenv("EVIDENTLY_TRACE_COLLECTOR_TEAM_ID", "")


_tracer: Optional[trace.Tracer] = None


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


def _create_tracer_provider(
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
    team_id: Optional[str] = None,
    export_id: Optional[str] = None,
) -> trace.TracerProvider:
    """
    Creates Evidently telemetry tracer provider which would be used for sending traces.
    Args:
        address: address of collector service
        exporter_type: type of exporter to use "grpc" or "http"
        api_key: authorization api key for Evidently tracing
        team_id: id of team in Evidently Cloud
        export_id: string id of exported data, all data with same id would be grouped into single dataset
    """
    global _tracer  # noqa: PLW0603

    _address = address or _TRACE_COLLECTOR_ADDRESS
    _exporter_type = exporter_type or _TRACE_COLLECTOR_TYPE
    _api_key = api_key or _TRACE_COLLECTOR_API_KEY
    _export_id = export_id or _TRACE_COLLECTOR_EXPORT_ID
    _team_id = team_id or _TRACE_COLLECTOR_TEAM_ID

    tracer_provider = TracerProvider(
        resource=Resource.create(
            {
                "evidently.export_id": _export_id,
                "evidently.team_id": _team_id,
            }
        )
    )
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
    return tracer_provider


def init_tracing(
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
    team_id: Optional[str] = None,
    export_id: Optional[str] = None,
    *,
    as_global: bool = True,
) -> trace.TracerProvider:
    """
    Initialize Evidently tracing
    Args:
        address: address of collector service
        exporter_type: type of exporter to use "grpc" or "http"
        api_key: authorization api key for Evidently tracing
        team_id: id of team in Evidently Cloud
        export_id: string id of exported data, all data with same id would be grouped into single dataset
        as_global: indicated when to register provider globally for opentelemetry of use local one
                   Can be useful when you don't want to mix already existing OpenTelemetry tracing with Evidently one,
                   but may require additional configuration
    """
    global _tracer  # noqa: PLW0603
    provider = _create_tracer_provider(address, exporter_type, api_key, team_id, export_id)

    if as_global:
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("evidently")
    else:
        _tracer = provider.get_tracer("evidently")
    return provider
