import datetime
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from evidently.core.metric_types import ByLabelValue
from evidently.core.metric_types import CountValue
from evidently.core.metric_types import MetricConfig
from evidently.core.metric_types import SingleValue
from evidently.core.serialization import ReportModel
from evidently.core.serialization import SnapshotModel
from evidently.legacy.core import new_id
from evidently.ui.service.base import Project
from evidently.ui.service.base import SeriesFilter
from evidently.ui.service.base import User
from evidently.ui.service.storage.sql.data import SQLDataStorage
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage
from evidently.ui.service.storage.sql.models import Base
from evidently.ui.service.storage.sql.models import PointSQLModel
from evidently.ui.service.type_aliases import ZERO_UUID


@pytest.fixture
def sqlite_engine():
    """Create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup: dispose engine to close all connections before deleting file
    # On Windows, SQLite locks the file until all connections are closed
    engine.dispose(close=True)

    import os
    import sys
    import time

    # On Windows, add a small delay to ensure file handles are released
    if sys.platform == "win32":
        time.sleep(0.1)

    # Retry deletion in case of permission errors (Windows-specific)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            os.unlink(db_path)
            break
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(0.1)
            else:
                raise


@pytest.fixture
def data_storage(sqlite_engine):
    """Create SQL data storage instance."""
    return SQLDataStorage(sqlite_engine)


@pytest.fixture
def metadata_storage(sqlite_engine):
    """Create SQL metadata storage instance."""
    return SQLProjectMetadataStorage(sqlite_engine)


@pytest.fixture
def test_user():
    """Create a test user."""
    return User(id=ZERO_UUID, name="Test User")


@pytest.fixture
def test_project():
    """Create a test project."""
    return Project(
        id=ZERO_UUID,
        name="Test Project",
        description="A test project",
    )


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def test_snapshot_id():
    """Create a test snapshot ID."""
    return new_id()


def create_single_value_snapshot(
    metric_id: str = "test-metric", value: float = 42.0, metric_type: str = "test_type"
) -> SnapshotModel:
    """Create a snapshot with a single value metric."""
    metric_result = SingleValue(value=value, display_name="Test Metric")
    metric_result.set_metric_location(
        MetricConfig(metric_id=metric_id, params={"type": metric_type, "column": "test_column"})
    )

    return SnapshotModel(
        report=ReportModel(items=[]),
        name="Test Snapshot",
        timestamp=datetime.datetime(2023, 1, 1, 0, 0, 0),
        metadata={},
        tags=[],
        metric_results={metric_id: metric_result},
        top_level_metrics=[],
        widgets=[],
        tests_widgets=[],
    )


def create_by_label_value_snapshot(metric_id: str = "test-metric") -> SnapshotModel:
    """Create a snapshot with a by-label value metric."""
    metric_result = ByLabelValue(
        display_name="Test By Label Metric",
        values={
            "label1": SingleValue(value=10.0, display_name="Label 1"),
            "label2": SingleValue(value=20.0, display_name="Label 2"),
        },
    )
    for label, val in metric_result.values.items():
        val.set_metric_location(
            MetricConfig(metric_id=metric_id, params={"type": "by_label", "column": "test_column", "label": label})
        )
    metric_result.set_metric_location(
        MetricConfig(metric_id=metric_id, params={"type": "by_label", "column": "test_column"})
    )

    return SnapshotModel(
        report=ReportModel(items=[]),
        name="Test Snapshot",
        timestamp=datetime.datetime(2023, 1, 1, 0, 0, 0),
        metadata={"env": "test"},
        tags=["prod"],
        metric_results={metric_id: metric_result},
        top_level_metrics=[],
        widgets=[],
        tests_widgets=[],
    )


def create_count_value_snapshot(metric_id: str = "test-metric") -> SnapshotModel:
    """Create a snapshot with a count value metric."""
    count = SingleValue(value=100.0, display_name="Count")
    share = SingleValue(value=0.5, display_name="Share")
    count.set_metric_location(MetricConfig(metric_id=metric_id, params={"type": "count", "column": "test_column"}))
    share.set_metric_location(MetricConfig(metric_id=metric_id, params={"type": "count", "column": "test_column"}))

    metric_result = CountValue(display_name="Test Count Metric", count=count, share=share)
    metric_result.set_metric_location(
        MetricConfig(metric_id=metric_id, params={"type": "count", "column": "test_column"})
    )

    return SnapshotModel(
        report=ReportModel(items=[]),
        name="Test Snapshot",
        timestamp=datetime.datetime(2023, 1, 2, 0, 0, 0),
        metadata={},
        tags=[],
        metric_results={metric_id: metric_result},
        top_level_metrics=[],
        widgets=[],
        tests_widgets=[],
    )


@pytest.mark.asyncio
async def test_add_snapshot_points_single_value(
    data_storage, sqlite_engine, metadata_storage, test_user, test_project_id
):
    """Test adding snapshot points with single value metric."""
    # Create project and snapshot first (required for foreign key constraints)
    project = Project(id=test_project_id, name="Test Project")
    await metadata_storage.add_project(project, test_user, org_id=None)

    snapshot = create_single_value_snapshot()
    snapshot_id = await metadata_storage.add_snapshot(test_project_id, snapshot)

    await data_storage.add_snapshot_points(test_project_id, snapshot_id, snapshot)

    # Verify point was stored
    with Session(sqlite_engine) as session:
        points = (
            session.execute(select(PointSQLModel).where(PointSQLModel.project_id == test_project_id)).scalars().all()
        )
        assert len(points) == 1
        assert points[0].value == 42.0
        assert points[0].metric_type == "test_type"
        assert points[0].snapshot_id == snapshot_id


@pytest.mark.asyncio
async def test_add_snapshot_points_by_label_value(
    data_storage, sqlite_engine, metadata_storage, test_user, test_project_id
):
    """Test adding snapshot points with by-label value metric."""
    # Create project and snapshot first (required for foreign key constraints)
    project = Project(id=test_project_id, name="Test Project")
    await metadata_storage.add_project(project, test_user, org_id=None)

    snapshot = create_by_label_value_snapshot()
    snapshot_id = await metadata_storage.add_snapshot(test_project_id, snapshot)

    await data_storage.add_snapshot_points(test_project_id, snapshot_id, snapshot)

    # Verify points were stored
    with Session(sqlite_engine) as session:
        points = (
            session.execute(select(PointSQLModel).where(PointSQLModel.project_id == test_project_id)).scalars().all()
        )
        assert len(points) == 2
        values = {p.value for p in points}
        assert values == {10.0, 20.0}


@pytest.mark.asyncio
async def test_add_snapshot_points_count_value(
    data_storage, sqlite_engine, metadata_storage, test_user, test_project_id
):
    """Test adding snapshot points with count value metric."""
    # Create project and snapshot first (required for foreign key constraints)
    project = Project(id=test_project_id, name="Test Project")
    await metadata_storage.add_project(project, test_user, org_id=None)

    snapshot = create_count_value_snapshot()
    snapshot_id = await metadata_storage.add_snapshot(test_project_id, snapshot)

    await data_storage.add_snapshot_points(test_project_id, snapshot_id, snapshot)

    # Verify points were stored (count and share)
    with Session(sqlite_engine) as session:
        points = (
            session.execute(select(PointSQLModel).where(PointSQLModel.project_id == test_project_id)).scalars().all()
        )
        assert len(points) == 2
        values = {p.value for p in points}
        assert values == {100.0, 0.5}


@pytest.mark.asyncio
async def test_get_metrics(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting available metrics."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot1 = create_single_value_snapshot(metric_id="metric1", metric_type="type1")
    snapshot2 = create_single_value_snapshot(metric_id="metric2", metric_type="type2")

    snapshot_id1 = await metadata_storage.add_snapshot(test_project.id, snapshot1)
    snapshot_id2 = await metadata_storage.add_snapshot(test_project.id, snapshot2)

    await data_storage.add_snapshot_points(test_project.id, snapshot_id1, snapshot1)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id2, snapshot2)

    metrics = await data_storage.get_metrics(test_project.id, tags=[], metadata={})
    assert len(metrics) == 2
    assert "type1" in metrics
    assert "type2" in metrics


@pytest.mark.asyncio
async def test_get_metrics_with_tags_filter(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting metrics filtered by tags."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot1 = create_single_value_snapshot(metric_id="metric1", metric_type="type1")
    snapshot2 = create_by_label_value_snapshot(metric_id="metric2")

    snapshot_id1 = await metadata_storage.add_snapshot(test_project.id, snapshot1)
    snapshot_id2 = await metadata_storage.add_snapshot(test_project.id, snapshot2)

    await data_storage.add_snapshot_points(test_project.id, snapshot_id1, snapshot1)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id2, snapshot2)

    # Filter by tags
    metrics = await data_storage.get_metrics(test_project.id, tags=["prod"], metadata={})
    assert len(metrics) == 1
    assert "by_label" in metrics


@pytest.mark.asyncio
async def test_get_metrics_with_metadata_filter(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting metrics filtered by metadata."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot1 = create_single_value_snapshot(metric_id="metric1", metric_type="type1")
    snapshot2 = create_by_label_value_snapshot(metric_id="metric2")

    snapshot_id1 = await metadata_storage.add_snapshot(test_project.id, snapshot1)
    snapshot_id2 = await metadata_storage.add_snapshot(test_project.id, snapshot2)

    await data_storage.add_snapshot_points(test_project.id, snapshot_id1, snapshot1)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id2, snapshot2)

    # Filter by metadata
    metrics = await data_storage.get_metrics(test_project.id, tags=[], metadata={"env": "test"})
    assert len(metrics) == 1
    assert "by_label" in metrics


@pytest.mark.asyncio
async def test_get_metric_labels(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting metric labels."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot = create_by_label_value_snapshot(metric_id="metric1")
    snapshot_id = await metadata_storage.add_snapshot(test_project.id, snapshot)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id, snapshot)

    labels = await data_storage.get_metric_labels(test_project.id, tags=[], metadata={}, metric="by_label")
    assert "label" in labels
    assert "column" in labels


@pytest.mark.asyncio
async def test_get_metric_label_values(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting metric label values."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot = create_by_label_value_snapshot(metric_id="metric1")
    snapshot_id = await metadata_storage.add_snapshot(test_project.id, snapshot)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id, snapshot)

    values = await data_storage.get_metric_label_values(
        test_project.id, tags=[], metadata={}, metric="by_label", label="label"
    )
    assert "label1" in values
    assert "label2" in values


@pytest.mark.asyncio
async def test_get_data_series(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting data series."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot1 = create_single_value_snapshot(metric_id="metric1", metric_type="type1", value=10.0)
    snapshot2 = create_single_value_snapshot(metric_id="metric1", metric_type="type1", value=20.0)

    snapshot_id1 = await metadata_storage.add_snapshot(test_project.id, snapshot1)
    snapshot_id2 = await metadata_storage.add_snapshot(test_project.id, snapshot2)

    await data_storage.add_snapshot_points(test_project.id, snapshot_id1, snapshot1)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id2, snapshot2)

    series_filter = [SeriesFilter(tags=[], metadata={}, metric="type1", metric_labels={})]

    response = await data_storage.get_data_series(test_project.id, series_filter, None, None)
    assert len(response.series) == 1
    assert len(response.series[0].values) == 2
    assert response.series[0].values == [10.0, 20.0]
    assert len(response.sources) == 2


@pytest.mark.asyncio
async def test_get_data_series_with_time_filter(data_storage, sqlite_engine, metadata_storage, test_user, test_project):
    """Test getting data series with time filter."""
    await metadata_storage.add_project(test_project, test_user, org_id=None)

    snapshot1 = create_single_value_snapshot(metric_id="metric1", metric_type="type1", value=10.0)
    snapshot1.timestamp = datetime.datetime(2023, 1, 1, 0, 0, 0)
    snapshot2 = create_single_value_snapshot(metric_id="metric1", metric_type="type1", value=20.0)
    snapshot2.timestamp = datetime.datetime(2023, 1, 3, 0, 0, 0)

    snapshot_id1 = await metadata_storage.add_snapshot(test_project.id, snapshot1)
    snapshot_id2 = await metadata_storage.add_snapshot(test_project.id, snapshot2)

    await data_storage.add_snapshot_points(test_project.id, snapshot_id1, snapshot1)
    await data_storage.add_snapshot_points(test_project.id, snapshot_id2, snapshot2)

    series_filter = [SeriesFilter(tags=[], metadata={}, metric="type1", metric_labels={})]

    # Filter by start time
    response = await data_storage.get_data_series(
        test_project.id, series_filter, datetime.datetime(2023, 1, 2, 0, 0, 0), None
    )
    assert len(response.series) == 1
    assert len(response.series[0].values) == 1
    assert response.series[0].values == [20.0]
