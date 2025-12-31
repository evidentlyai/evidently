import logging
import uuid
from collections import defaultdict
from enum import Enum
from typing import Annotated
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import litestar
from litestar import Router
from litestar.exceptions import HTTPException
from litestar.exceptions import NotFoundException
from litestar.params import Dependency
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2

from evidently._pydantic_compat import BaseModel
from evidently.core.datasets import ServiceColumns
from evidently.legacy.ui.type_aliases import UserID
from evidently.ui.service.datasets.metadata import DatasetTracingParams
from evidently.ui.service.managers.datasets import DatasetManager
from evidently.ui.service.tracing.storage.base import HumanFeedbackModel
from evidently.ui.service.tracing.storage.base import SpanModel
from evidently.ui.service.tracing.storage.base import TraceModel
from evidently.ui.service.tracing.storage.base import TracingStorage


class SessionDefinition(BaseModel):
    type: str = "session"
    session_field: str = "session_id"
    user_field: str = "user_id"
    time_split_sec: int = 30 * 60


@litestar.post("/")
async def export(
    user_id: UserID,
    request: litestar.Request,
    tracing_storage: TracingStorage,
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
) -> litestar.Response:
    data = await request.body()
    message = trace_service_pb2.ExportTraceServiceRequest()
    message.ParseFromString(data)
    export_id = None
    service_name = ""
    for resource in message.resource_spans:
        for res_attr in resource.resource.attributes:
            if res_attr.key == "service.name":
                service_name = res_attr.value.string_value
            if res_attr.key == "evidently.export_id":
                export_id = uuid.UUID(res_attr.value.string_value)
    if export_id is None:
        raise ValueError("Export ID is missing from trace data")

    tracing_storage.save(export_id, service_name, message)

    return litestar.Response(
        trace_service_pb2.ExportTraceServiceResponse().SerializeToString(),
        media_type="application/x-protobuf",
    )


@litestar.delete("/{export_id:uuid}/{trace_id:str}")
async def delete_trace(
    trace_id: str,
    tracing_storage: TracingStorage,
    user_id: UserID,
    export_id: uuid.UUID,
) -> None:
    await tracing_storage.delete_trace(export_id, trace_id)


def _get_first_span(trace: TraceModel) -> Optional[SpanModel]:
    for span in trace.spans:
        if span.parent_span_id == "":
            return span
    return None


class TraceListType(Enum):
    Auto = "auto"
    Ungrouped = "ungrouped"
    Session = "session"
    User = "user"


class TraceListGetterType(Enum):
    with_filters_from_metadata = "with_filters_from_metadata"
    ungrouped = "ungrouped"


class DatasetMetadata(BaseModel):
    id: uuid.UUID
    name: str
    params: Optional[DatasetTracingParams] = None


class TraceSessionsResponse(BaseModel):
    sessions: Dict[str, List[TraceModel]]
    metadata: DatasetMetadata


@litestar.post("/metadata")
async def update_metadata(
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    export_id: uuid.UUID,
    data: DatasetTracingParams,
) -> None:
    dataset = await dataset_manager.get_dataset_metadata(user_id, export_id)
    if dataset is None:
        raise NotFoundException(f"Dataset {export_id} not found")

    await dataset_manager.update_dataset_tracing_metadata(user_id, export_id, data)


@litestar.get("/list")
async def trace_sessions(
    tracing_storage: TracingStorage,
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    export_id: uuid.UUID,
    getter_type: TraceListGetterType,
) -> TraceSessionsResponse:
    traces = tracing_storage.read_traces_with_filter(export_id, None, None)
    dataset = await dataset_manager.get_dataset_metadata(user_id, export_id)
    if dataset is None:
        raise NotFoundException(f"Dataset {export_id} not found")

    metadata = DatasetMetadata(id=dataset.id, name=dataset.name)

    tracing_session_params = (
        await _determine_session_info(traces) if dataset.tracing_params is None else dataset.tracing_params
    )

    metadata.params = tracing_session_params

    if getter_type == TraceListGetterType.ungrouped:
        return TraceSessionsResponse(sessions={"undefined": traces}, metadata=metadata)

    type = TraceListType.Ungrouped
    if metadata.params.session_type is not None:
        type = TraceListType(tracing_session_params.session_type)

    session_field = metadata.params.session_field or "session_id"
    user_field = metadata.params.user_field or "user_id"
    time_split_sec = metadata.params.dialog_split_time_seconds or 30 * 60

    if type == TraceListType.Session:
        return TraceSessionsResponse(sessions=await _split_by_session(traces, session_field), metadata=metadata)
    if type == TraceListType.User:
        return TraceSessionsResponse(
            sessions=await _split_by_user(traces, user_field, time_split_sec), metadata=metadata
        )

    return TraceSessionsResponse(sessions={"undefined": traces}, metadata=metadata)


class AddHumanFeedbackRequest(BaseModel):
    trace_id: str
    feedback: HumanFeedbackModel


@litestar.post("/human_feedback")
async def add_human_feedback(
    tracing_storage: TracingStorage,
    dataset_manager: Annotated[DatasetManager, Dependency(skip_validation=True)],
    user_id: UserID,
    export_id: uuid.UUID,
    data: AddHumanFeedbackRequest,
) -> None:
    metadata = await dataset_manager.get_dataset_metadata(user_id, export_id)
    try:
        span_name = await tracing_storage.add_feedback(export_id, data.trace_id, data.feedback)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Human feedback supported only for SQLite storage")
    data_definition = metadata.data_definition
    if data_definition.service_columns is None:
        data_definition.service_columns = ServiceColumns()
    if (
        data_definition.service_columns.human_feedback_label is None
        or not data_definition.service_columns.human_feedback_label.startswith(span_name)
    ):
        if (
            data_definition.service_columns.human_feedback_label
            and data_definition.service_columns.human_feedback_label.startswith(span_name)
        ):
            logging.warning(
                f"{metadata.name} dataset has different human feedback label:"
                f" was: {data_definition.service_columns.human_feedback_label}, but expected:"
                f" {span_name}.human_feedback_label. Replacing it with a new one..."
            )
        data_definition.service_columns.human_feedback_label = f"{span_name}.human_feedback_label"
        data_definition.service_columns.human_feedback_comment = f"{span_name}.human_feedback_comment"
        await dataset_manager.update_dataset(user_id, export_id, None, None, data_definition, None, None)


async def _determine_session_info(traces: List[TraceModel]) -> DatasetTracingParams:
    sample = traces[:10]
    params = DatasetTracingParams()
    for trace in sample:
        span = _get_first_span(trace)
        if span is None:
            continue
        if params.session_type is None:
            if "session_id" in span.attributes:
                params.session_type = "session"
                params.session_field = "session_id"
            if "user_id" in span.attributes:
                params.session_type = "user"
                params.user_field = "user_id"
                params.dialog_split_time_seconds = 30 * 60
        if params.user_message_field is None:
            for possible_input_field in ["input", "question"]:
                if possible_input_field in span.attributes:
                    params.user_message_field = f"{span.span_name}:{possible_input_field}"
                    break
        if params.assistant_message_field is None:
            for possible_output_field in ["output", "answer", "result"]:
                if possible_output_field in span.attributes:
                    params.assistant_message_field = f"{span.span_name}:{possible_output_field}"
                    break
                if f"{possible_output_field}.data" in span.attributes:
                    params.assistant_message_field = f"{span.span_name}:{possible_output_field}.data"
                    break
    return params


async def _split_by_session(traces: List[TraceModel], session_field: str) -> Dict[str, List[TraceModel]]:
    result: Dict[str, List[TraceModel]] = defaultdict(list)
    for trace in traces:
        span = _get_first_span(trace)
        if span is None:
            continue
        session_id = str(span.attributes.get(session_field, "undefined"))
        result[session_id].append(trace)
    return result


async def _split_by_user(
    traces: List[TraceModel], user_field: str, dialog_split_sec: int
) -> Dict[str, List[TraceModel]]:
    result: Dict[str, List[TraceModel]] = defaultdict(list)
    traces_by_users: Dict[str, List[TraceModel]] = defaultdict(list)
    for trace in traces:
        span = _get_first_span(trace)
        if span is None:
            continue
        user_id = str(span.attributes.get(user_field, "undefined"))
        traces_by_users[user_id].append(trace)
    for user_id, user_traces in traces_by_users.items():
        start_time = user_traces[0].start_time.timestamp()
        session_id = user_id + f":{user_traces[0].start_time.isoformat()}"
        for trace in user_traces:
            trace_start = trace.start_time.timestamp()
            if (trace_start - start_time) > dialog_split_sec:
                session_id = user_id + f":{trace.start_time.isoformat()}"
            result[session_id].append(trace)
            start_time = trace_start
    return result


def tracing_api(guard: Callable) -> Router:
    return Router(
        "/v1/traces",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    trace_sessions,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    export,
                    delete_trace,
                    update_metadata,
                    add_human_feedback,
                ],
                guards=[guard],
            ),
        ],
    )
