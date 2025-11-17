import datetime
import tempfile
import uuid

import pytest
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.trace.v1 import trace_pb2
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from evidently.core.datasets import DataDefinition
from evidently.legacy.core import new_id
from evidently.ui.service.datasets.data_source import TracingDataSource
from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.datasets.metadata import FileDatasetMetadataStorage
from evidently.ui.service.tracing.storage.base import ExportID
from evidently.ui.service.tracing.storage.file import FileTracingStorage
from evidently.ui.service.tracing.storage.sql import SQLTracingStorage


@pytest.fixture
def tmp_path():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sqlite_engine():
    """Create a temporary SQLite database for testing."""
    import gc
    import os
    import sys
    import time

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    engine = create_engine(f"sqlite:///{db_path}", poolclass=NullPool)
    from evidently.ui.service.storage.sql.utils import migrate_database

    try:
        migrate_database(f"sqlite:///{db_path}")
    except Exception:
        from evidently.ui.service.tracing.storage.sql import TraceSpanModel

        TraceSpanModel.__table__.create(engine, checkfirst=True)

    yield engine

    engine.dispose(close=True)
    gc.collect()

    if sys.platform == "win32":
        time.sleep(0.2)

    max_retries = 10
    for attempt in range(max_retries):
        try:
            os.unlink(db_path)
            break
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(0.1 * (attempt + 1))
                gc.collect()
            else:
                if sys.platform == "win32":
                    import warnings

                    warnings.warn(f"Could not delete SQLite database file {db_path} on Windows.")
                else:
                    raise


@pytest.fixture
def file_storage(tmp_path, dataset_metadata_storage):
    """Create file-based tracing storage."""
    return FileTracingStorage(base_path=tmp_path)


@pytest.fixture
def sql_storage(sqlite_engine):
    """Create SQL-based tracing storage."""
    return SQLTracingStorage(engine=sqlite_engine)


@pytest.fixture
def project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def user_id():
    """Create a test user ID."""
    return new_id()


@pytest.fixture
def export_id():
    """Create a test export ID."""
    return new_id()


@pytest.fixture
def dataset_metadata_storage(tmp_path):
    """Create dataset metadata storage."""
    return FileDatasetMetadataStorage(base_path=tmp_path)


@pytest.fixture
def create_tracing_dataset(dataset_metadata_storage, project_id, user_id, export_id):
    """Create a tracing dataset metadata."""
    import asyncio

    dataset = DatasetMetadata(
        id=export_id,
        project_id=project_id,
        author_id=user_id,
        name="test-tracing-dataset",
        source=TracingDataSource(export_id=export_id),
        data_definition=DataDefinition(),
        description="",
        size_bytes=0,
        row_count=0,
        column_count=0,
        all_columns=[],
        is_draft=False,
        draft_params=None,
        origin=DatasetOrigin.tracing,
        metadata={},
        tags=[],
    )
    asyncio.run(dataset_metadata_storage.add_dataset_metadata(user_id, project_id, dataset))
    return dataset


@pytest.fixture
def trace_id():
    """Create a test trace ID."""
    return uuid.uuid4()


def create_test_trace_request(
    export_id: ExportID, trace_id: uuid.UUID, service_name: str = "test-service"
) -> trace_service_pb2.ExportTraceServiceRequest:
    """Create a test trace request."""
    request = trace_service_pb2.ExportTraceServiceRequest()

    resource_span = request.resource_spans.add()
    attr1 = resource_span.resource.attributes.add()
    attr1.key = "service.name"
    attr1.value.string_value = service_name
    attr2 = resource_span.resource.attributes.add()
    attr2.key = "evidently.export_id"
    attr2.value.string_value = str(export_id)

    scope_span = resource_span.scope_spans.add()
    scope_span.scope.name = "test-scope"

    span = scope_span.spans.add()
    span.trace_id = trace_id.bytes[:16]
    span_id_bytes = uuid.uuid4().bytes[:8]
    span.span_id = span_id_bytes
    span.parent_span_id = b""
    span.name = "test-span"
    span.kind = trace_pb2.Span.SpanKind.SPAN_KIND_SERVER
    now = datetime.datetime.now()
    span.start_time_unix_nano = int(now.timestamp() * 1000000000)
    span.end_time_unix_nano = int((now.timestamp() + 0.1) * 1000000000)

    attr1 = span.attributes.add()
    attr1.key = "input"
    attr1.value.string_value = "test input"
    attr2 = span.attributes.add()
    attr2.key = "output"
    attr2.value.string_value = "test output"
    attr3 = span.attributes.add()
    attr3.key = "session_id"
    attr3.value.string_value = "session-123"
    attr4 = span.attributes.add()
    attr4.key = "user_id"
    attr4.value.string_value = "user-456"

    return request


def create_test_trace_request_with_multiple_spans(
    export_id: ExportID, trace_id: uuid.UUID, service_name: str = "test-service"
) -> trace_service_pb2.ExportTraceServiceRequest:
    """Create a test trace request with multiple spans."""
    request = trace_service_pb2.ExportTraceServiceRequest()

    resource_span = request.resource_spans.add()
    attr1 = resource_span.resource.attributes.add()
    attr1.key = "service.name"
    attr1.value.string_value = service_name
    attr2 = resource_span.resource.attributes.add()
    attr2.key = "evidently.export_id"
    attr2.value.string_value = str(export_id)

    scope_span = resource_span.scope_spans.add()
    scope_span.scope.name = "test-scope"

    base_time = datetime.datetime.now()
    parent_span_id = uuid.uuid4().bytes[:8]

    span1 = scope_span.spans.add()
    span1.trace_id = trace_id.bytes[:16]
    span1.span_id = parent_span_id
    span1.parent_span_id = b""
    span1.name = "parent-span"
    span1.kind = trace_pb2.Span.SpanKind.SPAN_KIND_SERVER
    span1.start_time_unix_nano = int(base_time.timestamp() * 1000000000)
    span1.end_time_unix_nano = int((base_time.timestamp() + 0.2) * 1000000000)
    attr1 = span1.attributes.add()
    attr1.key = "session_id"
    attr1.value.string_value = "session-123"

    span2 = scope_span.spans.add()
    span2.trace_id = trace_id.bytes[:16]
    span2.span_id = uuid.uuid4().bytes[:8]
    span2.parent_span_id = parent_span_id
    span2.name = "child-span"
    span2.kind = trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL
    span2.start_time_unix_nano = int((base_time.timestamp() + 0.05) * 1000000000)
    span2.end_time_unix_nano = int((base_time.timestamp() + 0.15) * 1000000000)
    attr1 = span2.attributes.add()
    attr1.key = "input"
    attr1.value.string_value = "test input"
    attr2 = span2.attributes.add()
    attr2.key = "output"
    attr2.value.string_value = "test output"

    return request


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_save_trace(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test saving a trace."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 1
    assert traces[0].trace_id == str(trace_id)
    assert len(traces[0].spans) == 1
    assert traces[0].spans[0].span_name == "test-span"


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_save_multiple_traces(request, storage, export_id, create_tracing_dataset):
    """Test saving multiple traces."""
    storage_instance = request.getfixturevalue(storage)
    trace_id1 = uuid.uuid4()
    trace_id2 = uuid.uuid4()

    trace_request1 = create_test_trace_request(export_id, trace_id1)
    trace_request2 = create_test_trace_request(export_id, trace_id2)

    storage_instance.save(export_id, "test-service", trace_request1)
    storage_instance.save(export_id, "test-service", trace_request2)

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 2
    trace_ids = {t.trace_id for t in traces}
    assert str(trace_id1) in trace_ids
    assert str(trace_id2) in trace_ids


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_read_as_dataframe(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test reading traces as DataFrame."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    df = storage_instance.read_as_dataframe(export_id)
    assert not df.empty
    assert "id" in df.columns
    assert "timestamp" in df.columns
    assert len(df) == 1
    assert str(df.iloc[0]["id"]) == str(trace_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
async def test_get_data_definition(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test getting data definition."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    data_definition, columns = await storage_instance.get_data_definition(export_id)
    assert data_definition is not None
    assert len(columns) > 0
    assert "id" in columns
    assert "timestamp" in columns


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_read_with_filter_timestamp(request, storage, export_id, create_tracing_dataset):
    """Test reading traces with timestamp filter."""
    storage_instance = request.getfixturevalue(storage)
    trace_id1 = uuid.uuid4()
    trace_id2 = uuid.uuid4()

    base_time = datetime.datetime.now()
    trace_request1 = create_test_trace_request(export_id, trace_id1)
    trace_request2 = create_test_trace_request(export_id, trace_id2)

    storage_instance.save(export_id, "test-service", trace_request1)
    storage_instance.save(export_id, "test-service", trace_request2)

    timestamp_from = base_time - datetime.timedelta(seconds=1)
    timestamp_to = base_time + datetime.timedelta(seconds=1)

    df = storage_instance.read_with_filter(export_id, timestamp_from, timestamp_to, None, None)
    assert len(df) >= 1


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_read_traces_with_filter(request, storage, export_id, create_tracing_dataset):
    """Test reading traces with filter."""
    storage_instance = request.getfixturevalue(storage)
    trace_id1 = uuid.uuid4()
    trace_id2 = uuid.uuid4()

    base_time = datetime.datetime.now()
    trace_request1 = create_test_trace_request(export_id, trace_id1)
    trace_request2 = create_test_trace_request(export_id, trace_id2)

    storage_instance.save(export_id, "test-service", trace_request1)
    storage_instance.save(export_id, "test-service", trace_request2)

    timestamp_from = base_time - datetime.timedelta(seconds=1)
    timestamp_to = base_time + datetime.timedelta(seconds=1)

    traces = storage_instance.read_traces_with_filter(export_id, timestamp_from, timestamp_to)
    assert len(traces) >= 1


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_read_traces_with_multiple_spans(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test reading traces with multiple spans."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request_with_multiple_spans(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 1
    assert len(traces[0].spans) == 2

    span_names = {span.span_name for span in traces[0].spans}
    assert "parent-span" in span_names
    assert "child-span" in span_names


@pytest.mark.asyncio
@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
async def test_delete_trace(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test deleting a trace."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    traces_before = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces_before) == 1

    await storage_instance.delete_trace(export_id, str(trace_id))

    traces_after = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces_after) == 0


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_get_trace_range_for_run(request, storage, export_id, create_tracing_dataset):
    """Test getting trace range for a run."""
    storage_instance = request.getfixturevalue(storage)
    trace_id1 = uuid.uuid4()
    trace_id2 = uuid.uuid4()

    base_time = datetime.datetime.now()
    trace_request1 = create_test_trace_request(export_id, trace_id1)
    trace_request2 = create_test_trace_request(export_id, trace_id2)

    storage_instance.save(export_id, "test-service", trace_request1)
    storage_instance.save(export_id, "test-service", trace_request2)

    start_time = base_time - datetime.timedelta(seconds=1)
    end_time = base_time + datetime.timedelta(seconds=1)

    max_trace_id = storage_instance.get_trace_range_for_run(0, start_time, end_time)
    assert max_trace_id is not None


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_read_empty_export_id(request, storage, export_id):
    """Test reading from non-existent export ID."""
    storage_instance = request.getfixturevalue(storage)

    df = storage_instance.read_as_dataframe(export_id)
    assert df.empty

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 0


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_append_mode(request, storage, export_id, create_tracing_dataset):
    """Test that file storage supports append mode."""
    storage_instance = request.getfixturevalue(storage)
    trace_id1 = uuid.uuid4()
    trace_id2 = uuid.uuid4()

    trace_request1 = create_test_trace_request(export_id, trace_id1)
    trace_request2 = create_test_trace_request(export_id, trace_id2)

    storage_instance.save(export_id, "test-service", trace_request1)
    storage_instance.save(export_id, "test-service", trace_request2)

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 2


@pytest.mark.parametrize("storage", ["file_storage", "sql_storage"])
def test_trace_attributes_preserved(request, storage, export_id, trace_id, create_tracing_dataset):
    """Test that trace attributes are preserved."""
    storage_instance = request.getfixturevalue(storage)
    trace_request = create_test_trace_request(export_id, trace_id)

    storage_instance.save(export_id, "test-service", trace_request)

    traces = storage_instance.read_traces_with_filter(export_id, None, None)
    assert len(traces) == 1
    trace = traces[0]

    assert trace.trace_id == str(trace_id)
    assert len(trace.spans) == 1
    span = trace.spans[0]

    assert span.span_name == "test-span"
    assert "input" in span.attributes
    assert "output" in span.attributes
    assert span.attributes["input"] == "test input"
    assert span.attributes["output"] == "test output"
    assert span.attributes["session_id"] == "session-123"
    assert span.attributes["user_id"] == "user-456"
