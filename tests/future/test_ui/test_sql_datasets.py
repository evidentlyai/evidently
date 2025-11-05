import datetime

import pandas as pd
import pytest
import pytest_asyncio

from evidently.core.datasets import Dataset
from evidently.legacy.core import new_id
from evidently.ui.service.datasets.data_source import FileDataSource
from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.storage.sql.dataset import SQLDatasetMetadataStorage


@pytest.fixture
def dataset_metadata_storage(sqlite_engine):
    """Create SQL dataset metadata storage instance."""
    return SQLDatasetMetadataStorage(sqlite_engine)


@pytest_asyncio.fixture
async def setup_user_and_project(metadata_storage, test_user, test_project_id):
    """Set up test user and project in database."""
    from evidently.ui.service.base import Project

    project = Project(
        id=test_project_id,
        name="Test Project",
        description="Test",
        created_at=datetime.datetime.now(),
    )
    await metadata_storage.add_project(project, test_user, org_id=None)


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})


@pytest.fixture
def sample_dataset_metadata(test_project_id, test_user, sample_dataframe):
    """Create a sample dataset metadata."""
    df = sample_dataframe
    data_def = Dataset.from_pandas(df).data_definition
    return DatasetMetadata(
        id=new_id(),
        project_id=test_project_id,
        author_id=test_user.id,
        name="test_dataset",
        description="Test dataset",
        data_definition=data_def,
        source=FileDataSource(project_id=test_project_id, filename="test_file.parquet"),
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


@pytest.mark.asyncio
async def test_add_dataset_metadata(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test adding dataset metadata."""
    dataset_id = await dataset_metadata_storage.add_dataset_metadata(
        test_user.id, test_project_id, sample_dataset_metadata
    )
    assert dataset_id == sample_dataset_metadata.id


@pytest.mark.asyncio
async def test_get_dataset_metadata(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test retrieving dataset metadata."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    retrieved = await dataset_metadata_storage.get_dataset_metadata(sample_dataset_metadata.id)
    assert retrieved is not None
    assert retrieved.id == sample_dataset_metadata.id
    assert retrieved.name == sample_dataset_metadata.name
    assert retrieved.description == sample_dataset_metadata.description
    assert retrieved.project_id == test_project_id


@pytest.mark.asyncio
async def test_update_dataset_metadata(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test updating dataset metadata."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    sample_dataset_metadata.name = "updated_name"
    sample_dataset_metadata.description = "updated_description"
    await dataset_metadata_storage.update_dataset_metadata(sample_dataset_metadata.id, sample_dataset_metadata)
    retrieved = await dataset_metadata_storage.get_dataset_metadata(sample_dataset_metadata.id)
    assert retrieved.name == "updated_name"
    assert retrieved.description == "updated_description"


@pytest.mark.asyncio
async def test_list_datasets_metadata(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test listing datasets metadata."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    datasets = await dataset_metadata_storage.list_datasets_metadata(test_project_id, None, None, None)
    assert len(datasets) == 1
    assert datasets[0].id == sample_dataset_metadata.id


@pytest.mark.asyncio
async def test_mark_dataset_deleted(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test soft deleting a dataset."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    await dataset_metadata_storage.mark_dataset_deleted(sample_dataset_metadata.id)
    retrieved = await dataset_metadata_storage.get_dataset_metadata(sample_dataset_metadata.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_datasets_count(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test counting datasets."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    count = await dataset_metadata_storage.datasets_count(test_project_id)
    assert count == 1


@pytest.mark.asyncio
async def test_list_datasets_filter_by_origin(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test filtering datasets by origin."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    datasets = await dataset_metadata_storage.list_datasets_metadata(test_project_id, None, [DatasetOrigin.file], None)
    assert len(datasets) == 1
    datasets = await dataset_metadata_storage.list_datasets_metadata(
        test_project_id, None, [DatasetOrigin.dataset], None
    )
    assert len(datasets) == 0


@pytest.mark.asyncio
async def test_list_datasets_filter_by_draft(
    dataset_metadata_storage, setup_user_and_project, test_user, test_project_id, sample_dataset_metadata
):
    """Test filtering datasets by draft status."""
    await dataset_metadata_storage.add_dataset_metadata(test_user.id, test_project_id, sample_dataset_metadata)
    datasets = await dataset_metadata_storage.list_datasets_metadata(test_project_id, None, None, False)
    assert len(datasets) == 1
    datasets = await dataset_metadata_storage.list_datasets_metadata(test_project_id, None, None, True)
    assert len(datasets) == 0
