import uuid
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import pandas as pd
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from sqlalchemy import Engine
from sqlalchemy import Index
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.ui.service.storage.sql.base import BaseSQLStorage
from evidently.ui.service.storage.sql.models import Base
from evidently.ui.service.tracing.storage.base import ExportID
from evidently.ui.service.tracing.storage.base import HumanFeedbackModel
from evidently.ui.service.tracing.storage.base import SpanModel
from evidently.ui.service.tracing.storage.base import TraceModel
from evidently.ui.service.tracing.storage.base import TracingStorage
from evidently.ui.service.tracing.storage.base import _enrich_span_usage

EVIDENTLY_TRACE_LINK_COLUMN_NAME = "_evidently_trace_link"


class TraceSpanModel(Base):
    """SQL model for trace spans."""

    __tablename__ = "trace_spans"
    __table_args__ = (
        Index("trace_spans_export_id_idx", "export_id"),
        Index("trace_spans_trace_id_idx", "trace_id"),
        Index("trace_spans_timestamp_idx", "timestamp"),
    )

    timestamp: Mapped[datetime] = mapped_column(index=True, nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trace_id: Mapped[uuid.UUID] = mapped_column(index=True)
    export_id: Mapped[uuid.UUID] = mapped_column(index=True)
    trace_state: Mapped[str]
    span_id: Mapped[str]
    parent_span_id: Mapped[Optional[str]]
    span_name: Mapped[str]
    span_kind: Mapped[str]
    scope_name: Mapped[str]
    service_name: Mapped[str]
    resource_attributes: Mapped[Dict[str, Any]]
    span_attributes: Mapped[Dict[str, Any]]
    end_time: Mapped[Optional[datetime]]


def convert_to_value(value):
    """Convert protobuf value to Python value."""
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, (common_pb2.ArrayValue,)):
        return [convert_to_value(getattr(v, v.WhichOneof("value"))) for v in value.values]
    return str(value)


class SQLTracingStorage(BaseSQLStorage, TracingStorage):
    """SQL-based tracing storage implementation."""

    def __init__(self, engine: Engine):
        BaseSQLStorage.__init__(self, engine)
        from evidently.ui.service.storage.sql.utils import migrate_database

        try:
            migrate_database(str(engine.url))
        except Exception:
            TraceSpanModel.__table__.create(engine, checkfirst=True)

    @classmethod
    def provide(cls, engine: Engine) -> "TracingStorage":  # type: ignore[override]
        """Provide instance for dependency injection."""
        return cls(engine)

    def save(
        self,
        export_id: ExportID,
        service_name: Optional[str],
        trace: trace_service_pb2.ExportTraceServiceRequest,
    ) -> None:
        """Save trace data to SQL storage."""
        with self.session as session:
            for resource in trace.resource_spans:
                for scope in resource.scope_spans:
                    for span in scope.spans:
                        session.execute(
                            insert(TraceSpanModel),
                            [
                                {
                                    "timestamp": datetime.fromtimestamp(span.start_time_unix_nano / 1000000000.0),
                                    "trace_id": uuid.UUID(bytes=span.trace_id),
                                    "export_id": export_id,
                                    "trace_state": span.trace_state,
                                    "span_id": span.span_id.hex(),
                                    "parent_span_id": span.parent_span_id.hex() if span.parent_span_id else "",
                                    "span_name": span.name,
                                    "end_time": (
                                        datetime.fromtimestamp(span.end_time_unix_nano / 1000000000.0)
                                        if span.end_time_unix_nano
                                        else None
                                    ),
                                    "span_kind": span.SpanKind.Name(span.kind),
                                    "scope_name": scope.scope.name if scope.scope else "",
                                    "service_name": service_name or "",
                                    "resource_attributes": {
                                        attr.key: convert_to_value(getattr(attr.value, attr.value.WhichOneof("value")))
                                        for attr in resource.resource.attributes
                                    },
                                    "span_attributes": {
                                        attr.key: convert_to_value(getattr(attr.value, attr.value.WhichOneof("value")))
                                        for attr in span.attributes
                                    },
                                }
                            ],
                        )
            session.commit()

    def read_as_dataframe(self, export_id: ExportID) -> pd.DataFrame:
        """Read traces as DataFrame."""
        with self.session as session:
            data = session.scalars(
                select(TraceSpanModel)
                .where(TraceSpanModel.export_id == export_id)
                .order_by(TraceSpanModel.trace_id, TraceSpanModel.timestamp)
                .limit(10000),
            ).all()
            return _convert_to_dataframe(export_id, data)

    async def get_data_definition(self, export_id: ExportID) -> Tuple[DataDefinition, List[str]]:
        """Get data definition for traces."""
        with self.session as session:
            data = session.scalars(
                select(TraceSpanModel)
                .where(TraceSpanModel.export_id == export_id)
                .order_by(TraceSpanModel.trace_id, TraceSpanModel.timestamp)
                .limit(1000),
            ).all()
            df = _convert_to_dataframe(export_id, data)
            dataset = Dataset.from_pandas(df)
            return dataset.data_definition, df.columns.tolist()

    def read_with_filter(
        self,
        export_id: ExportID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
        id_from: Optional[int] = None,
        id_to: Optional[int] = None,
    ) -> pd.DataFrame:
        """Read traces with filters."""
        if timestamp_from is None and timestamp_to is None and id_from is None and id_to is None:
            return self.read_as_dataframe(export_id)

        filters = [TraceSpanModel.export_id == export_id]
        if timestamp_from is not None:
            filters.append(TraceSpanModel.timestamp >= timestamp_from)
        if timestamp_to is not None:
            filters.append(TraceSpanModel.timestamp <= timestamp_to)
        if id_from is not None:
            filters.append(TraceSpanModel.id > id_from)
        if id_to is not None:
            filters.append(TraceSpanModel.id <= id_to)

        with self.session as session:
            data = session.scalars(
                select(TraceSpanModel).where(and_(*filters)).order_by(TraceSpanModel.trace_id, TraceSpanModel.timestamp)
            ).all()
            return _convert_to_dataframe(export_id, data)

    def get_trace_range_for_run(self, start_id: int, start_time: datetime, end_time: datetime) -> Optional[uuid.UUID]:
        """Get trace range for a run."""
        with self.session as session:
            max_id = session.execute(
                select(func.max(TraceSpanModel.trace_id)).where(
                    and_(
                        TraceSpanModel.id > start_id,
                        TraceSpanModel.timestamp >= start_time,
                        TraceSpanModel.timestamp <= end_time,
                    )
                )
            ).scalar()
            return max_id

    def read_traces_with_filter(
        self,
        export_id: ExportID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
    ) -> List[TraceModel]:
        """Read traces with filter as TraceModel list."""
        filters = [TraceSpanModel.export_id == export_id]
        if timestamp_from is not None:
            filters.append(TraceSpanModel.timestamp >= timestamp_from)
        if timestamp_to is not None:
            filters.append(TraceSpanModel.timestamp <= timestamp_to)
        with self.session as session:
            data = session.scalars(
                select(TraceSpanModel).where(and_(*filters)).order_by(TraceSpanModel.trace_id, TraceSpanModel.timestamp)
            ).all()
            return _collect_trace(data)

    async def delete_trace(self, export_id: ExportID, trace_id: str) -> None:
        """Delete a trace."""
        with self.session as session:
            session.execute(
                delete(TraceSpanModel)
                .where(TraceSpanModel.trace_id == uuid.UUID(trace_id))
                .where(TraceSpanModel.export_id == export_id)
            )
            session.commit()

    async def add_feedback(self, export_id: ExportID, trace_id: str, feedback: HumanFeedbackModel) -> str:
        with self.session as session:
            stmt = select(TraceSpanModel).where(
                TraceSpanModel.trace_id == uuid.UUID(trace_id),
                TraceSpanModel.export_id == export_id,
                TraceSpanModel.parent_span_id == "",
            )
            data = session.scalar(stmt)
            new_attributes = data.span_attributes.copy()

            new_attributes["human_feedback_label"] = feedback.label
            new_attributes["human_feedback_comment"] = feedback.comment
            data.span_attributes = new_attributes
            session.commit()
            return data.span_name


def _collect_trace(data: Sequence[TraceSpanModel]) -> List[TraceModel]:
    """Collect spans into TraceModel objects."""
    traces = []
    trace: Optional[TraceModel] = None
    for item in data:
        trace_id = str(item.trace_id)
        if trace is None or trace.trace_id != trace_id:
            if trace is not None:
                trace.end_time = None if len(trace.spans) == 0 else trace.spans[-1].end_time
                traces.append(trace)
            trace = TraceModel(
                trace_id=trace_id,
                attributes={
                    k: str(v) for (k, v) in item.resource_attributes.items() if isinstance(v, (str, int, float, bool))
                },
                spans=[],
                start_time=item.timestamp,
                end_time=None,
            )
        span = SpanModel(
            span_id=item.span_id,
            parent_span_id=item.parent_span_id or "",
            span_name=item.span_name,
            start_time=item.timestamp,
            end_time=item.end_time,
            attributes={k: str(v) for (k, v) in item.span_attributes.items() if isinstance(v, (str, int, float, bool))},
        )
        _enrich_span_usage(span)
        trace.spans.append(span)
    if trace is not None:
        trace.end_time = None if len(trace.spans) == 0 else trace.spans[-1].end_time
        # Sort spans by start_time before appending trace
        trace.spans.sort(key=lambda s: s.start_time)
        traces.append(trace)
    traces.sort(key=lambda t: t.start_time)
    return traces


def _collect_trace_for_dataframe(export_id: uuid.UUID, data: Sequence[TraceSpanModel]) -> List[dict]:
    """Collect traces into dictionary format for DataFrame."""
    traces = []
    trace: Optional[dict] = None
    for row in data:
        trace_id = row.trace_id
        if trace is not None:
            if trace["id"] != trace_id:
                traces.append(trace)
                trace = {
                    "id": trace_id,
                    "timestamp": row.timestamp,
                    EVIDENTLY_TRACE_LINK_COLUMN_NAME: f"{str(export_id)}/{trace_id}",
                }
        else:
            trace = {
                "id": trace_id,
                "service_name": row.service_name,
                "timestamp": row.timestamp,
                EVIDENTLY_TRACE_LINK_COLUMN_NAME: f"{str(export_id)}/{trace_id}",
            }
        for key, value in row.span_attributes.items():
            if isinstance(value, (str, int, float, bool)):
                trace[f"{row.span_name}.{key}"] = value
            if key.startswith("tokens."):
                token_id = key.split(".", 1)[1]
                trace[f"total_tokens.{token_id}"] = trace.get(f"total_tokens.{token_id}", 0) + int(value)
            if key.startswith("cost."):
                token_id = key.split(".", 1)[1]
                trace[f"total_cost.{token_id}"] = trace.get(f"total_cost.{token_id}", 0) + float(value)
    if trace is not None:
        traces.append(trace)
    return traces


def _convert_to_dataframe(export_id: uuid.UUID, data: Sequence[TraceSpanModel]) -> pd.DataFrame:
    """Convert trace spans to DataFrame."""
    df = pd.DataFrame(_collect_trace_for_dataframe(export_id, data))
    if not df.empty:
        df = df.sort_values(by="timestamp", ascending=True)
    return df
