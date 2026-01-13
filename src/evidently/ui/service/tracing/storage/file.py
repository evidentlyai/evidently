import json
import posixpath
import uuid
import warnings
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from fsspec.implementations.local import LocalFileSystem
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.ui.service.errors import DatasetNotFound
from evidently.ui.service.storage.fslocation import FSLocation
from evidently.ui.service.tracing.storage.base import ExportID
from evidently.ui.service.tracing.storage.base import HumanFeedbackModel
from evidently.ui.service.tracing.storage.base import SpanModel
from evidently.ui.service.tracing.storage.base import TraceModel
from evidently.ui.service.tracing.storage.base import TracingStorage
from evidently.ui.service.tracing.storage.base import _enrich_span_usage

EVIDENTLY_TRACE_LINK_COLUMN_NAME = "_evidently_trace_link"


def _convert_protobuf_to_trace_model(
    export_id: ExportID, service_name: Optional[str], trace_request: trace_service_pb2.ExportTraceServiceRequest
) -> List[TraceModel]:
    """Convert protobuf trace request to TraceModel list."""
    traces_dict: dict[str, TraceModel] = {}

    for resource in trace_request.resource_spans:
        resource_attrs = {attr.key: _convert_protobuf_value(attr.value) for attr in resource.resource.attributes}

        for scope in resource.scope_spans:
            for span in scope.spans:
                trace_id = str(uuid.UUID(bytes=span.trace_id))
                span_id = span.span_id.hex()
                parent_span_id = span.parent_span_id.hex() if span.parent_span_id else ""

                start_time = datetime.fromtimestamp(span.start_time_unix_nano / 1000000000.0)
                end_time = (
                    datetime.fromtimestamp(span.end_time_unix_nano / 1000000000.0) if span.end_time_unix_nano else None
                )

                span_attrs = {attr.key: _convert_protobuf_value(attr.value) for attr in span.attributes}

                span_model = SpanModel(
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    span_name=span.name,
                    start_time=start_time,
                    end_time=end_time,
                    attributes=span_attrs,
                )

                if trace_id not in traces_dict:
                    traces_dict[trace_id] = TraceModel(
                        trace_id=trace_id,
                        start_time=start_time,
                        end_time=end_time,
                        attributes=resource_attrs,
                        spans=[],
                    )

                traces_dict[trace_id].spans.append(span_model)
                if traces_dict[trace_id].start_time > start_time:
                    traces_dict[trace_id].start_time = start_time
                if end_time is not None:
                    current_end_time = traces_dict[trace_id].end_time
                    if current_end_time is None:
                        traces_dict[trace_id].end_time = end_time
                    elif current_end_time < end_time:
                        traces_dict[trace_id].end_time = end_time

    return list(traces_dict.values())


def _convert_protobuf_value(value) -> Union[str, int, float, list]:
    """Convert protobuf value to Python value."""
    which = value.WhichOneof("value")
    if which == "string_value":
        return value.string_value
    elif which == "int_value":
        return value.int_value
    elif which == "double_value":
        return value.double_value
    elif which == "bool_value":
        return str(value.bool_value)
    elif which == "array_value":
        return [_convert_protobuf_value(v) for v in value.array_value.values]
    else:
        return str(value)


class FileTracingStorage(TracingStorage):
    """File system-based tracing storage using JSONL files."""

    def __init__(self, base_path: str, force_append: bool = False):
        self.base_path = base_path
        self.force_append = force_append
        self._location: Optional[FSLocation] = None
        self._append_warning_shown = False

    @property
    def location(self) -> FSLocation:
        """Get or create FSLocation."""
        if self._location is None:
            self._location = FSLocation(self.base_path)
        return self._location

    def _supports_append(self) -> bool:
        """Check if the filesystem supports append mode."""
        # If force_append is set, use append mode regardless of filesystem
        if self.force_append:
            return True
        # Only LocalFileSystem supports append mode
        return isinstance(self.location.fs, LocalFileSystem)

    def _get_trace_file_path(self, export_id: ExportID) -> str:
        """Get the file path for a trace dataset.

        Stores trace files in the dataset directory: {project_id}/datasets/{export_id}/traces.jsonl
        """
        # Find project_id by searching for the dataset (export_id is the dataset_id)
        project_id = self._find_project_id_for_dataset(export_id)
        return posixpath.join(str(project_id), "datasets", str(export_id), "traces.jsonl")

    def _find_project_id_for_dataset(self, dataset_id: DatasetID) -> ProjectID:
        """Find project_id for a dataset by searching the filesystem."""
        from evidently.ui.service.datasets.metadata import UUID_REGEX

        # Search all projects for the dataset
        for project_dir in self.location.listdir(""):
            if not UUID_REGEX.match(project_dir):
                continue
            project_id = project_dir
            datasets_dir = posixpath.join(project_id, "datasets")
            if not self.location.exists(datasets_dir):
                continue

            for dataset_dir in self.location.listdir(datasets_dir):
                if not UUID_REGEX.match(dataset_dir):
                    continue
                if dataset_dir == str(dataset_id):
                    return project_id
        raise DatasetNotFound()

    @classmethod
    def provide(cls, base_path: str, force_append: bool = False) -> "TracingStorage":  # type: ignore[override]
        """Provide instance for dependency injection."""
        return cls(base_path, force_append=force_append)

    def save(
        self,
        export_id: ExportID,
        service_name: Optional[str],
        trace: trace_service_pb2.ExportTraceServiceRequest,
    ) -> None:
        """Save trace data to JSONL file."""
        trace_models = _convert_protobuf_to_trace_model(export_id, service_name, trace)
        file_path = self._get_trace_file_path(export_id)

        self.location.makedirs(posixpath.dirname(file_path))

        if self._supports_append():
            # Use append mode for filesystems that support it (local filesystem)
            with self.location.open(file_path, "a") as f:
                for trace_model in trace_models:
                    json_line = trace_model.json()
                    f.write(json_line + "\n")
        else:
            # For non-LocalFileSystem, use read-modify-write pattern
            if not self._append_warning_shown:
                fs_name = type(self.location.fs).__name__
                protocol = getattr(self.location.fs, "protocol", None)
                fs_desc = f"{fs_name}" + (f" ({protocol})" if protocol else "")
                warnings.warn(
                    f"Filesystem {fs_desc} does not support append mode. "
                    "Using read-modify-write which may be slow for large files. "
                    "Consider using SQL storage for better performance with object storage backends, "
                    "or set force_append=True if you want to use append mode anyway",
                    UserWarning,
                    stacklevel=2,
                )
                self._append_warning_shown = True

            # Read existing traces
            existing_traces_dict: dict[str, TraceModel] = {}
            if self.location.exists(file_path):
                with self.location.open(file_path, "r") as f:
                    for line in f:
                        if line.strip():
                            trace_dict = json.loads(line)
                            trace_model = TraceModel(**trace_dict)
                            existing_traces_dict[trace_model.trace_id] = trace_model

            # Merge new traces with existing ones
            for trace_model in trace_models:
                trace_id = trace_model.trace_id
                if trace_id in existing_traces_dict:
                    # Merge spans from this trace into the existing one
                    existing_trace = existing_traces_dict[trace_id]
                    existing_trace.spans.extend(trace_model.spans)
                    # Update start_time to be the earliest
                    if trace_model.start_time < existing_trace.start_time:
                        existing_trace.start_time = trace_model.start_time
                    # Update end_time to be the latest
                    if trace_model.end_time is not None:
                        if existing_trace.end_time is None or trace_model.end_time > existing_trace.end_time:
                            existing_trace.end_time = trace_model.end_time
                else:
                    existing_traces_dict[trace_id] = trace_model

            # Write all traces back
            with self.location.open(file_path, "w") as f:
                for trace_model in existing_traces_dict.values():
                    json_line = trace_model.json()
                    f.write(json_line + "\n")

    def read_as_dataframe(self, export_id: ExportID) -> pd.DataFrame:
        """Read traces as DataFrame."""
        try:
            file_path = self._get_trace_file_path(export_id)
        except DatasetNotFound:
            # Dataset not found, return empty DataFrame
            return pd.DataFrame()
        if not self.location.exists(file_path):
            return pd.DataFrame()

        traces_dict: dict[str, TraceModel] = {}
        with self.location.open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    trace_dict = json.loads(line)
                    trace_model = TraceModel(**trace_dict)
                    trace_id = trace_model.trace_id

                    if trace_id not in traces_dict:
                        traces_dict[trace_id] = trace_model
                    else:
                        # Merge spans from this trace into the existing one
                        existing_trace = traces_dict[trace_id]
                        existing_trace.spans.extend(trace_model.spans)
                        # Update start_time to be the earliest
                        if trace_model.start_time < existing_trace.start_time:
                            existing_trace.start_time = trace_model.start_time
                        # Update end_time to be the latest
                        if trace_model.end_time is not None:
                            if existing_trace.end_time is None or trace_model.end_time > existing_trace.end_time:
                                existing_trace.end_time = trace_model.end_time

        # Sort spans within each trace by start_time
        for trace in traces_dict.values():
            trace.spans.sort(key=lambda s: s.start_time)

        traces = [_trace_to_dict(export_id, trace) for trace in traces_dict.values()]
        df = pd.DataFrame(traces)
        if not df.empty:
            df = df.sort_values(by="timestamp", ascending=True)
        return df

    async def get_data_definition(self, export_id: ExportID) -> Tuple[DataDefinition, List[str]]:
        """Get data definition for traces."""
        try:
            df = self.read_as_dataframe(export_id)
        except DatasetNotFound:
            # Dataset not found, return empty data definition
            return DataDefinition(), []
        if df.empty:
            return DataDefinition(), []
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
        try:
            file_path = self._get_trace_file_path(export_id)
        except DatasetNotFound:
            # Dataset not found, return empty DataFrame
            return pd.DataFrame()
        if not self.location.exists(file_path):
            return pd.DataFrame()

        traces_dict: dict[str, TraceModel] = {}
        line_num = 0
        with self.location.open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    line_num += 1
                    if id_from is not None and line_num <= id_from:
                        continue
                    if id_to is not None and line_num > id_to:
                        break

                    trace_dict = json.loads(line)
                    trace_model = TraceModel(**trace_dict)

                    if timestamp_from is not None and trace_model.start_time < timestamp_from:
                        continue
                    if timestamp_to is not None and trace_model.start_time > timestamp_to:
                        continue

                    trace_id = trace_model.trace_id
                    if trace_id not in traces_dict:
                        traces_dict[trace_id] = trace_model
                    else:
                        # Merge spans from this trace into the existing one
                        existing_trace = traces_dict[trace_id]
                        existing_trace.spans.extend(trace_model.spans)
                        # Update start_time to be the earliest
                        if trace_model.start_time < existing_trace.start_time:
                            existing_trace.start_time = trace_model.start_time
                        # Update end_time to be the latest
                        if trace_model.end_time is not None:
                            if existing_trace.end_time is None or trace_model.end_time > existing_trace.end_time:
                                existing_trace.end_time = trace_model.end_time

        # Sort spans within each trace by start_time
        for trace in traces_dict.values():
            trace.spans.sort(key=lambda s: s.start_time)

        traces = [_trace_to_dict(export_id, trace) for trace in traces_dict.values()]
        df = pd.DataFrame(traces)
        if not df.empty:
            df = df.sort_values(by="timestamp", ascending=True)
        return df

    def get_trace_range_for_run(self, start_id: int, start_time: datetime, end_time: datetime) -> Optional[uuid.UUID]:
        """Get trace range for a run."""
        from evidently.ui.service.datasets.metadata import UUID_REGEX

        def check_trace_file(file_path: str) -> Optional[uuid.UUID]:
            """Check a trace file and return max trace_id within time range."""
            if not self.location.exists(file_path):
                return None

            max_trace_id = None
            line_num = 0
            with self.location.open(file_path, "r") as f:
                for line in f:
                    if line.strip():
                        line_num += 1
                        if line_num <= start_id:
                            continue

                        trace_dict = json.loads(line)
                        trace_model = TraceModel(**trace_dict)

                        if trace_model.start_time >= start_time and trace_model.start_time <= end_time:
                            try:
                                trace_uuid = uuid.UUID(trace_model.trace_id)
                                if max_trace_id is None or trace_uuid > max_trace_id:
                                    max_trace_id = trace_uuid
                            except ValueError:
                                pass
            return max_trace_id

        # Search all project/datasets directories for trace files
        max_trace_id = None
        for project_dir in self.location.listdir(""):
            if not UUID_REGEX.match(project_dir):
                continue
            datasets_dir = posixpath.join(project_dir, "datasets")
            if not self.location.exists(datasets_dir):
                continue

            for dataset_dir in self.location.listdir(datasets_dir):
                if not UUID_REGEX.match(dataset_dir):
                    continue

                file_path = posixpath.join(project_dir, "datasets", dataset_dir, "traces.jsonl")
                file_max = check_trace_file(file_path)
                if file_max is not None:
                    if max_trace_id is None or file_max > max_trace_id:
                        max_trace_id = file_max

        return max_trace_id

    def read_traces_with_filter(
        self,
        export_id: ExportID,
        timestamp_from: Optional[datetime],
        timestamp_to: Optional[datetime],
    ) -> List[TraceModel]:
        """Read traces with filter as TraceModel list."""
        try:
            file_path = self._get_trace_file_path(export_id)
        except DatasetNotFound:
            # Dataset not found, return empty list
            return []
        if not self.location.exists(file_path):
            return []

        traces_dict: dict[str, TraceModel] = {}
        with self.location.open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    trace_dict = json.loads(line)
                    trace_model = TraceModel(**trace_dict)

                    if timestamp_from is not None and trace_model.start_time < timestamp_from:
                        continue
                    if timestamp_to is not None and trace_model.start_time > timestamp_to:
                        continue

                    trace_id = trace_model.trace_id
                    if trace_id not in traces_dict:
                        traces_dict[trace_id] = trace_model
                    else:
                        # Merge spans from this trace into the existing one
                        existing_trace = traces_dict[trace_id]
                        existing_trace.spans.extend(trace_model.spans)
                        # Update start_time to be the earliest
                        if trace_model.start_time < existing_trace.start_time:
                            existing_trace.start_time = trace_model.start_time
                        # Update end_time to be the latest
                        if trace_model.end_time is not None:
                            if existing_trace.end_time is None or trace_model.end_time > existing_trace.end_time:
                                existing_trace.end_time = trace_model.end_time

        # Sort spans within each trace by start_time
        for trace in traces_dict.values():
            trace.spans.sort(key=lambda s: s.start_time)
            for span in trace.spans:
                _enrich_span_usage(span)

        traces = list(traces_dict.values())
        traces.sort(key=lambda t: t.start_time)
        return traces

    async def delete_trace(self, export_id: ExportID, trace_id: str) -> None:
        """Delete a trace by rewriting the file without that trace."""
        try:
            file_path = self._get_trace_file_path(export_id)
        except DatasetNotFound:
            # Dataset not found, nothing to delete
            return
        if not self.location.exists(file_path):
            return

        temp_file_path = file_path + ".tmp"
        found = False

        with self.location.open(file_path, "r") as f_in, self.location.open(temp_file_path, "w") as f_out:
            for line in f_in:
                if line.strip():
                    trace_dict = json.loads(line)
                    trace_model = TraceModel(**trace_dict)
                    if trace_model.trace_id != trace_id:
                        f_out.write(line)
                    else:
                        found = True

        if found:
            self.location.rmtree(file_path)
            with self.location.open(temp_file_path, "r") as f_in, self.location.open(file_path, "w") as f_out:
                for line in f_in:
                    f_out.write(line)
            self.location.rmtree(temp_file_path)

    async def add_feedback(self, export_id: ExportID, trace_id: str, feedback: HumanFeedbackModel) -> str:
        """Add a feedback to the trace."""
        raise NotImplementedError()


def _trace_to_dict(export_id: ExportID, trace: TraceModel) -> dict:
    """Convert TraceModel to dictionary for DataFrame."""
    result = {
        "id": trace.trace_id,
        "timestamp": trace.start_time,
        EVIDENTLY_TRACE_LINK_COLUMN_NAME: f"{str(export_id)}/{trace.trace_id}",
    }

    result.update(trace.attributes)

    for span in trace.spans:
        for key, value in span.attributes.items():
            if isinstance(value, (str, int, float, bool)):
                result[f"{span.span_name}.{key}"] = value
            if key.startswith("tokens."):
                token_id = key.split(".", 1)[1]
                if isinstance(value, (int, float)):
                    current_total = result.get(f"total_tokens.{token_id}", 0)
                    if isinstance(current_total, int):
                        result[f"total_tokens.{token_id}"] = current_total + int(value)
                    else:
                        result[f"total_tokens.{token_id}"] = int(value)
            if key.startswith("cost."):
                token_id = key.split(".", 1)[1]
                if isinstance(value, (int, float)):
                    current_total = result.get(f"total_cost.{token_id}", 0.0)
                    if isinstance(current_total, (int, float)):
                        result[f"total_cost.{token_id}"] = float(current_total) + float(value)
                    else:
                        result[f"total_cost.{token_id}"] = float(value)

    return result
