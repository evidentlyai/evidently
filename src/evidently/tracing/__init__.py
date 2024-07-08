import os
import urllib.parse
import uuid
from functools import wraps
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

import requests
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from evidently.ui.workspace.cloud import ACCESS_TOKEN_COOKIE
from evidently.ui.workspace.cloud import CloudMetadataStorage

_TRACE_COLLECTOR_ADDRESS = os.getenv("EVIDENTLY_TRACE_COLLECTOR", "https://app.evidently.cloud")
_TRACE_COLLECTOR_TYPE = os.getenv("EVIDENTLY_TRACE_COLLECTOR_TYPE", "http")
_TRACE_COLLECTOR_API_KEY = os.getenv("EVIDENTLY_TRACE_COLLECTOR_API_KEY", "")
_TRACE_COLLECTOR_EXPORT_NAME = os.getenv("EVIDENTLY_TRACE_COLLECTOR_EXPORT_NAME", "")
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


class _EvidentlyPartialClient:
    def __init__(self, base_url: str, token: Optional[str]):
        pass

    def jwt_token(self) -> str:
        if not self._jwt_token_valid():
            self._update_jwt_token()
        return self._jwt_token

    def get_or_create_dataset(self, name: str) -> Optional[uuid.UUID]:
        pass


def _create_tracer_provider(
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
    team_id: Optional[str] = None,
    export_name: Optional[str] = None,
) -> trace.TracerProvider:
    """
    Creates Evidently telemetry tracer provider which would be used for sending traces.
    Args:
        address: address of collector service
        exporter_type: type of exporter to use "grpc" or "http"
        api_key: authorization api key for Evidently tracing
        team_id: id of team in Evidently Cloud
        export_name: string name of exported data, all data with same id would be grouped into single dataset
    """
    global _tracer  # noqa: PLW0603

    _address = address or _TRACE_COLLECTOR_ADDRESS
    if len(_address) == 0:
        raise ValueError(
            "You need to provide valid trace collector address with "
            "argument address or EVIDENTLY_TRACE_COLLECTOR env variable"
        )
    _exporter_type = exporter_type or _TRACE_COLLECTOR_TYPE
    if _exporter_type != "http":
        raise ValueError("Only 'http' exporter_type is supported")
    _api_key = api_key or _TRACE_COLLECTOR_API_KEY
    _export_name = export_name or _TRACE_COLLECTOR_EXPORT_NAME
    if len(_export_name) == 0:
        raise ValueError(
            "You need to provide export name with export_name argument"
            " or EVIDENTLY_TRACE_COLLECTOR_EXPORT_NAME env variable"
        )
    _team_id = team_id or _TRACE_COLLECTOR_TEAM_ID
    try:
        uuid.UUID(_team_id)
    except ValueError:
        raise ValueError(
            "You need provide valid team ID with team_id argument" "or EVIDENTLY_TRACE_COLLECTOR_TEAM_ID env variable"
        )

    cloud = CloudMetadataStorage(_address, _api_key, ACCESS_TOKEN_COOKIE.key)
    datasets = cloud._request("/api/datasets", "GET").json()["datasets"]
    _export_id = None
    for dataset in datasets:
        if dataset["name"] == _export_name:
            _export_id = dataset["id"]
            break
    if _export_id is None:
        resp = cloud._request(
            "/api/datasets/tracing",
            "POST",
            query_params={"team_id": _team_id},
            body={"name": _export_name},
        )

        _export_id = resp.json()["dataset_id"]

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

        session = requests.Session()

        def refresh_token(r, *args, **kwargs):
            if r.status_code == 401:
                cloud._jwt_token = None
                token = cloud.jwt_token
                session.headers.update({"Authorization": f"Bearer {token}"})
                r.request.headers["Authorization"] = session.headers["Authorization"]
                return session.send(r.request, verify=False)

        session.hooks["response"].append(refresh_token)

        exporter = OTLPSpanExporter(
            urllib.parse.urljoin(_address, "/v1/traces"),
            headers=dict([] if _api_key is None else [("authorization", _api_key)]),
            session=session,
        )
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    _tracer = tracer_provider.get_tracer("evidently")
    return tracer_provider


def init_tracing(
    address: Optional[str] = None,
    exporter_type: Optional[str] = None,
    api_key: Optional[str] = None,
    team_id: Optional[str] = None,
    export_name: Optional[str] = None,
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
        export_name: string name of exported data, all data with same id would be grouped into single dataset
        as_global: indicated when to register provider globally for opentelemetry of use local one
                   Can be useful when you don't want to mix already existing OpenTelemetry tracing with Evidently one,
                   but may require additional configuration
    """
    global _tracer  # noqa: PLW0603
    provider = _create_tracer_provider(address, exporter_type, api_key, team_id, export_name)

    if as_global:
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("evidently")
    else:
        _tracer = provider.get_tracer("evidently")
    return provider
