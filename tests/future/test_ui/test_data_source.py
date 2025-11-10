from io import BytesIO
from unittest.mock import AsyncMock

import pandas as pd
import pytest

from evidently.legacy.core import new_id
from evidently.ui.service.datasets.data_source import DatasetDataSource
from evidently.ui.service.datasets.data_source import FileDataSource
from evidently.ui.service.storage.local.base import FSSpecBlobStorage
from evidently.ui.service.storage.local.dataset import DatasetFileStorage
from evidently.ui.service.type_aliases import ZERO_UUID


@pytest.fixture
def tmp_path():
    """Create a temporary directory."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def blob_storage(tmp_path):
    """Create blob storage."""
    return FSSpecBlobStorage(base_path=tmp_path)


@pytest.fixture
def dataset_file_storage(blob_storage):
    """Create dataset file storage."""
    return DatasetFileStorage(dataset_blob_storage=blob_storage)


@pytest.fixture
def test_user_id():
    """Create a test user ID."""
    return ZERO_UUID


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def test_dataset_id():
    """Create a test dataset ID."""
    return new_id()


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe."""
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})


@pytest.fixture
def sample_parquet_data(sample_dataframe):
    """Create sample parquet data."""
    buf = BytesIO()
    sample_dataframe.to_parquet(buf, engine="pyarrow")
    return buf.getvalue()


@pytest.fixture
def dataset_manager_mock(
    dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_parquet_data, sample_dataframe
):
    """Create a mock dataset manager."""
    from unittest.mock import MagicMock

    from evidently.ui.service.managers.datasets import DatasetManager

    manager = MagicMock(spec=DatasetManager)
    manager.dataset_file_storage = dataset_file_storage

    # Store the file in storage
    blob_id = dataset_file_storage.put_dataset(
        test_user_id, test_project_id, test_dataset_id, "test.parquet", sample_parquet_data
    )

    # Mock get_dataset_metadata to return metadata with the file source
    from evidently.core.datasets import Dataset
    from evidently.ui.service.datasets.metadata import DatasetMetadata
    from evidently.ui.service.datasets.metadata import DatasetOrigin

    df = sample_dataframe
    data_def = Dataset.from_pandas(df).data_definition
    metadata = DatasetMetadata(
        id=test_dataset_id,
        project_id=test_project_id,
        author_id=test_user_id,
        name="test_dataset",
        description="Test",
        source=FileDataSource(project_id=test_project_id, filename=blob_id),
        data_definition=data_def,
        size_bytes=100,
        row_count=len(df),
        column_count=len(df.columns),
        all_columns=list(df.columns),
        is_draft=False,
        draft_params=None,
        origin=DatasetOrigin.file,
        metadata={},
        tags=[],
    )

    async def get_dataset_metadata(user_id, dataset_id):
        if dataset_id == test_dataset_id:
            return metadata
        return None

    manager.get_dataset_metadata = AsyncMock(side_effect=get_dataset_metadata)
    return manager


@pytest.mark.asyncio
async def test_file_data_source_materialize(
    dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_parquet_data, sample_dataframe
):
    """Test FileDataSource.materialize()."""
    from unittest.mock import MagicMock

    from evidently.ui.service.managers.datasets import DatasetManager
    from evidently.ui.service.managers.projects import ProjectManager

    # Store the file
    blob_id = dataset_file_storage.put_dataset(
        test_user_id, test_project_id, test_dataset_id, "test.parquet", sample_parquet_data
    )

    # Create a minimal dataset manager mock
    project_manager = MagicMock(spec=ProjectManager)
    dataset_manager = DatasetManager(
        project_manager=project_manager,
        dataset_metadata=MagicMock(),
        dataset_file_storage=dataset_file_storage,
    )

    # Create FileDataSource pointing to the stored file
    file_source = FileDataSource(project_id=test_project_id, filename=blob_id)

    # Materialize the data source
    df = await file_source.materialize(dataset_manager)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2"]
    pd.testing.assert_frame_equal(df, sample_dataframe)


@pytest.mark.asyncio
async def test_file_data_source_materialize_missing_file(dataset_file_storage, test_project_id):
    """Test FileDataSource.materialize() with missing file."""
    from unittest.mock import MagicMock

    from evidently.ui.service.datasets.data_source import DatasetReadError
    from evidently.ui.service.managers.datasets import DatasetManager

    project_manager = MagicMock()
    dataset_manager = DatasetManager(
        project_manager=project_manager,
        dataset_metadata=MagicMock(),
        dataset_file_storage=dataset_file_storage,
    )

    file_source = FileDataSource(project_id=test_project_id, filename="nonexistent/file.parquet")

    with pytest.raises(DatasetReadError):
        await file_source.materialize(dataset_manager)


@pytest.mark.asyncio
async def test_dataset_data_source_materialize(dataset_manager_mock, test_user_id, test_dataset_id, sample_dataframe):
    """Test DatasetDataSource.materialize()."""
    dataset_source = DatasetDataSource(
        user_id=test_user_id,
        dataset_id=test_dataset_id,
        filter_by=None,
        sort_by=None,
    )

    df = await dataset_source.materialize(dataset_manager_mock)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2"]
    pd.testing.assert_frame_equal(df, sample_dataframe)


@pytest.mark.asyncio
async def test_dataset_data_source_materialize_with_filters(dataset_manager_mock, test_user_id, test_dataset_id):
    """Test DatasetDataSource.materialize() with filters."""
    from evidently.ui.service.datasets.filters import EqualFilter

    dataset_source = DatasetDataSource(
        user_id=test_user_id,
        dataset_id=test_dataset_id,
        filter_by=[EqualFilter(column="col1", value=1)],
        sort_by=None,
    )

    df = await dataset_source.materialize(dataset_manager_mock)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[0]["col2"] == "a"


@pytest.mark.asyncio
async def test_dataset_data_source_materialize_with_sorting(dataset_manager_mock, test_user_id, test_dataset_id):
    """Test DatasetDataSource.materialize() with sorting."""
    from evidently.ui.service.datasets.data_source import SortBy

    dataset_source = DatasetDataSource(
        user_id=test_user_id,
        dataset_id=test_dataset_id,
        filter_by=None,
        sort_by=SortBy(column="col1", ascending=False),
    )

    df = await dataset_source.materialize(dataset_manager_mock)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df["col1"].values) == [3, 2, 1]  # Sorted descending


@pytest.mark.asyncio
async def test_dataset_data_source_materialize_missing_dataset(dataset_manager_mock, test_user_id):
    """Test DatasetDataSource.materialize() with missing dataset."""
    from evidently.legacy.core import new_id
    from evidently.ui.service.datasets.data_source import DatasetReadError

    dataset_source = DatasetDataSource(
        user_id=test_user_id,
        dataset_id=new_id(),
        filter_by=None,
        sort_by=None,
    )

    with pytest.raises(DatasetReadError, match="not found"):
        await dataset_source.materialize(dataset_manager_mock)
