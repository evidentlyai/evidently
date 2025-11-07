import datetime
from io import BytesIO
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pandas as pd
import pytest
from litestar.datastructures import UploadFile

from evidently.core.datasets import Dataset
from evidently.legacy.core import new_id
from evidently.ui.service.datasets.metadata import DatasetMetadata
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.managers.datasets import DatasetManager
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.storage.local.base import FSSpecBlobStorage
from evidently.ui.service.storage.local.dataset import DatasetFileStorage
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


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
def dataset_metadata_storage():
    """Create in-memory dataset metadata storage for testing."""
    from collections import defaultdict
    from typing import Dict

    class InMemoryDatasetMetadataStorage(DatasetMetadataStorage):
        def __init__(self):
            self._datasets: Dict[DatasetID, DatasetMetadata] = {}
            self._project_datasets: Dict[ProjectID, list[DatasetID]] = defaultdict(list)

        async def add_dataset_metadata(
            self, user_id: UserID, project_id: ProjectID, dataset: DatasetMetadata
        ) -> DatasetID:
            self._datasets[dataset.id] = dataset
            self._project_datasets[project_id].append(dataset.id)
            return dataset.id

        async def update_dataset_metadata(self, dataset_id: DatasetID, new_metadata: DatasetMetadata):
            if dataset_id in self._datasets:
                stored = self._datasets[dataset_id]
                stored.name = new_metadata.name
                stored.description = new_metadata.description
                stored.data_definition = new_metadata.data_definition
                stored.metadata = new_metadata.metadata
                stored.tags = new_metadata.tags

        async def update_dataset_tracing_metadata(self, dataset_id: DatasetID, tracing_metadata):
            pass

        async def get_dataset_metadata(self, dataset_id: DatasetID):
            from evidently.ui.service.datasets.metadata import DatasetMetadataFull

            if dataset_id not in self._datasets:
                return None
            ds = self._datasets[dataset_id]
            return DatasetMetadataFull(
                id=ds.id,
                project_id=ds.project_id,
                author_id=ds.author_id,
                name=ds.name,
                description=ds.description,
                data_definition=ds.data_definition,
                source=ds.source,
                size_bytes=ds.size_bytes,
                row_count=ds.row_count,
                column_count=ds.column_count,
                all_columns=ds.all_columns,
                is_draft=ds.is_draft,
                draft_params=ds.draft_params,
                origin=ds.origin,
                metadata=ds.metadata,
                tags=ds.tags,
                tracing_params=ds.tracing_params,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                author_name="Test User",
            )

        async def mark_dataset_deleted(self, dataset_id: DatasetID):
            if dataset_id in self._datasets:
                del self._datasets[dataset_id]

        async def delete_dataset_metadata(self, dataset_id: DatasetID):
            if dataset_id in self._datasets:
                del self._datasets[dataset_id]

        async def list_datasets_metadata(self, project_id: ProjectID, limit, origin, draft) -> list:
            from evidently.ui.service.datasets.metadata import DatasetMetadataFull

            result = []
            for ds_id in self._project_datasets.get(project_id, []):
                if ds_id in self._datasets:
                    ds = self._datasets[ds_id]
                    if origin and ds.origin not in origin:
                        continue
                    if draft is not None and ds.is_draft != draft:
                        continue
                    result.append(
                        DatasetMetadataFull(
                            id=ds.id,
                            project_id=ds.project_id,
                            author_id=ds.author_id,
                            name=ds.name,
                            description=ds.description,
                            data_definition=ds.data_definition,
                            source=ds.source,
                            size_bytes=ds.size_bytes,
                            row_count=ds.row_count,
                            column_count=ds.column_count,
                            all_columns=ds.all_columns,
                            is_draft=ds.is_draft,
                            draft_params=ds.draft_params,
                            origin=ds.origin,
                            metadata=ds.metadata,
                            tags=ds.tags,
                            tracing_params=ds.tracing_params,
                            created_at=datetime.datetime.now(),
                            updated_at=datetime.datetime.now(),
                            author_name="Test User",
                        )
                    )
            return result[:limit] if limit else result

        async def datasets_count(self, project_id: ProjectID) -> int:
            return len(self._project_datasets.get(project_id, []))

    return InMemoryDatasetMetadataStorage()


@pytest.fixture
def mock_project_manager():
    """Create a mock project manager."""
    from unittest.mock import AsyncMock

    pm = MagicMock(spec=ProjectManager)
    pm.get_project = AsyncMock(return_value=None)
    return pm


@pytest.fixture
def dataset_manager(dataset_metadata_storage, dataset_file_storage, mock_project_manager):
    """Create dataset manager."""
    return DatasetManager(
        project_manager=mock_project_manager,
        dataset_metadata=dataset_metadata_storage,
        dataset_file_storage=dataset_file_storage,
    )


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe."""
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})


@pytest.fixture
def sample_upload_file(sample_dataframe):
    """Create a sample upload file."""
    buf = BytesIO()
    sample_dataframe.to_csv(buf, index=False)
    buf.seek(0)
    return UploadFile(
        content_type="text/csv",
        filename="test.csv",
        file_data=buf.getvalue(),
    )


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def test_user_id():
    """Create a test user ID."""
    return ZERO_UUID


@pytest.mark.asyncio
async def test_upload_dataset_from_dataframe(
    dataset_manager, dataset_metadata_storage, sample_dataframe, test_user_id, test_project_id, mock_project_manager
):
    """Test uploading a dataset from a dataframe."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    dataset = await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    assert dataset.name == "test_dataset"
    assert dataset.description == "Test description"
    assert dataset.row_count == len(sample_dataframe)


@pytest.mark.asyncio
async def test_upload_dataset_from_file(
    dataset_manager,
    dataset_metadata_storage,
    sample_upload_file,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test uploading a dataset from an upload file."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(pd.DataFrame()).data_definition
    dataset = await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_upload_file,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    assert dataset.name == "test_dataset"
    assert dataset.row_count == 3


@pytest.mark.asyncio
async def test_get_dataset_metadata_not_found(dataset_manager, test_user_id):
    """Test getting non-existent dataset metadata."""
    with pytest.raises(ValueError, match="not found"):
        await dataset_manager.get_dataset_metadata(test_user_id, new_id())


@pytest.mark.asyncio
async def test_update_dataset(
    dataset_manager,
    dataset_metadata_storage,
    sample_dataframe,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test updating a dataset."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    dataset = await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    await dataset_manager.update_dataset(
        test_user_id, dataset.id, "updated_name", "updated_description", None, None, None
    )
    updated = await dataset_manager.get_dataset_metadata(test_user_id, dataset.id)
    assert updated.name == "updated_name"
    assert updated.description == "updated_description"


@pytest.mark.asyncio
async def test_delete_dataset(
    dataset_manager,
    dataset_metadata_storage,
    sample_dataframe,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test deleting a dataset."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    dataset = await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    await dataset_manager.delete_dataset(test_user_id, dataset.id)
    with pytest.raises(ValueError, match="not found"):
        await dataset_manager.get_dataset_metadata(test_user_id, dataset.id)


@pytest.mark.asyncio
async def test_list_datasets(
    dataset_manager,
    dataset_metadata_storage,
    sample_dataframe,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test listing datasets."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    datasets = await dataset_manager.list_datasets(test_user_id, test_project_id, None, None, None)
    assert len(datasets) == 1


@pytest.mark.asyncio
async def test_get_dataset_pagination(
    dataset_manager,
    dataset_metadata_storage,
    sample_dataframe,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test getting paginated dataset data."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    dataset = await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    pagination = await dataset_manager.get_dataset_pagination(test_user_id, dataset.id, 2, 1, None, None)
    assert pagination.page_size == 2
    assert pagination.current_page == 1
    assert len(pagination.items) == 2
    assert pagination.total_pages == 2


@pytest.mark.asyncio
async def test_datasets_count(
    dataset_manager,
    dataset_metadata_storage,
    sample_dataframe,
    test_user_id,
    test_project_id,
    mock_project_manager,
):
    """Test counting datasets."""
    from evidently.ui.service.base import Project

    mock_project_manager.get_project = AsyncMock(return_value=Project(id=test_project_id, name="Test"))
    data_def = Dataset.from_pandas(sample_dataframe).data_definition
    await dataset_manager.upload_dataset(
        test_user_id,
        test_project_id,
        "test_dataset",
        "Test description",
        sample_dataframe,
        data_def,
        DatasetOrigin.file,
        {},
        [],
    )
    count = await dataset_manager.datasets_count(test_user_id, test_project_id)
    assert count == 1
