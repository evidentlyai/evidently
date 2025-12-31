import abc
import uuid
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from typing_extensions import TypeAlias

from evidently._pydantic_compat import BaseModel
from evidently.core.datasets import DataDefinition


class SpanModel(BaseModel):
    span_id: str
    span_name: str
    parent_span_id: str
    start_time: datetime
    end_time: Optional[datetime]
    attributes: Dict[str, Union[str, int, float]]


class TraceModel(BaseModel):
    trace_id: str
    start_time: datetime
    end_time: Optional[datetime]
    attributes: Dict[str, Union[str, int, float]]
    spans: List[SpanModel]


class HumanFeedbackModel(BaseModel):
    label: Optional[str]
    comment: Optional[str]


ExportID: TypeAlias = uuid.UUID


class TracingStorage(abc.ABC):
    @abc.abstractmethod
    def save(
        self,
        export_id: ExportID,
        service_name: Optional[str],
        trace: trace_service_pb2.ExportTraceServiceRequest,
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_as_dataframe(self, export_id: ExportID) -> pd.DataFrame:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_data_definition(self, export_id: ExportID) -> Tuple[DataDefinition, List[str]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_with_filter(
        self,
        export_id: ExportID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
        id_from: Optional[int] = None,
        id_to: Optional[int] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_traces_with_filter(
        self,
        export_id: uuid.UUID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
    ) -> List[TraceModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_trace_range_for_run(self, start_id: int, start_time: datetime, end_time: datetime) -> Optional[uuid.UUID]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_trace(self, export_id: ExportID, trace_id: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_feedback(self, export_id: ExportID, trace_id: str, feedback: HumanFeedbackModel) -> str:
        """
        adds a feedback to the trace for given export_id
        Args:
            export_id:
            trace_id:
            feedback:

        Returns:
            span name where the feedback was added
        """
        raise NotImplementedError()


def _enrich_span_usage(span: SpanModel) -> None:
    if "openinference.span.kind" in span.attributes:  # assume this span is from openinference instrumentor
        if "llm.token_count.completion" in span.attributes:
            # completion tokens is output
            span.attributes["tokens.output"] = span.attributes["llm.token_count.completion"]
        if "llm.token_count.prompt" in span.attributes:
            # prompt tokens is input
            span.attributes["tokens.input"] = span.attributes["llm.token_count.prompt"]


class NoopTracingStorage(TracingStorage):
    def get_trace_range_for_run(self, start_id: int, start_time: datetime, end_time: datetime) -> Optional[uuid.UUID]:
        return None

    def save(
        self,
        export_id: ExportID,
        service_name: Optional[str],
        trace: trace_service_pb2.ExportTraceServiceRequest,
    ) -> None:
        pass

    def read_as_dataframe(self, export_id: ExportID) -> pd.DataFrame:
        return pd.DataFrame()

    async def get_data_definition(self, export_id: ExportID) -> Tuple[DataDefinition, List[str]]:
        return DataDefinition(), []

    def read_with_filter(
        self,
        export_id: ExportID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
        id_from: Optional[int] = None,
        id_to: Optional[int] = None,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    def read_traces_with_filter(
        self, export_id: uuid.UUID, timestamp_from: Optional[datetime], timestamp_to: Optional[datetime]
    ) -> List[TraceModel]:
        return []

    async def delete_trace(self, export_id: ExportID, trace_id: str) -> None:
        return

    async def add_feedback(self, export_id: ExportID, trace_id: str, feedback: HumanFeedbackModel) -> str:
        raise NotImplementedError()

    @classmethod
    def provide(cls) -> "TracingStorage":
        return cls()
