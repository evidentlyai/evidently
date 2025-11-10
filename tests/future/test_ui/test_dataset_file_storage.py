import pytest

from evidently.legacy.core import new_id
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
def sample_data():
    """Create sample data."""
    return b"id,name\n1,test\n2,example"


def test_put_dataset(dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_data):
    """Test storing a dataset file."""
    blob_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, test_dataset_id, "test.csv", sample_data)
    assert blob_id is not None
    assert "datasets" in blob_id
    assert str(test_project_id) in blob_id
    assert str(test_dataset_id) in blob_id
    assert "test.csv" in blob_id


def test_get_dataset(dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_data):
    """Test retrieving a dataset file."""
    blob_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, test_dataset_id, "test.csv", sample_data)
    retrieved = dataset_file_storage.get_dataset(blob_id)
    assert retrieved == sample_data


def test_check_dataset(dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_data):
    """Test checking if a dataset file exists."""
    blob_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, test_dataset_id, "test.csv", sample_data)
    assert dataset_file_storage.check_dataset(blob_id) is True
    assert dataset_file_storage.check_dataset("nonexistent/blob/id") is False


def test_remove_dataset(dataset_file_storage, test_user_id, test_project_id, test_dataset_id, sample_data):
    """Test removing a dataset file."""
    blob_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, test_dataset_id, "test.csv", sample_data)
    assert dataset_file_storage.check_dataset(blob_id) is True
    dataset_file_storage.remove_dataset(blob_id)
    assert dataset_file_storage.check_dataset(blob_id) is False


def test_get_dataset_blob_id(dataset_file_storage, test_project_id, test_dataset_id):
    """Test getting dataset blob ID."""
    blob_id = DatasetFileStorage.get_dataset_blob_id(test_project_id, test_dataset_id, "test_file.csv")
    assert "datasets" in blob_id
    assert str(test_project_id) in blob_id
    assert str(test_dataset_id) in blob_id
    assert "test_file.csv" in blob_id
