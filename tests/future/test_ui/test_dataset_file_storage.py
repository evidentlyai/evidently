import pytest

from evidently.legacy.core import new_id
from evidently.ui.service.storage.local.dataset import FSSpecDatasetFileStorage
from evidently.ui.service.type_aliases import ZERO_UUID


@pytest.fixture
def tmp_path():
    """Create a temporary directory."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def dataset_file_storage(tmp_path):
    """Create dataset file storage."""
    return FSSpecDatasetFileStorage(base_path=tmp_path)


@pytest.fixture
def test_user_id():
    """Create a test user ID."""
    return ZERO_UUID


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def sample_data():
    """Create sample data."""
    return b"id,name\n1,test\n2,example"


def test_put_dataset(dataset_file_storage, test_user_id, test_project_id, sample_data):
    """Test storing a dataset file."""
    file_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, "test.csv", sample_data)
    assert file_id is not None
    assert str(test_user_id) in str(file_id)


def test_get_dataset(dataset_file_storage, test_user_id, test_project_id, sample_data):
    """Test retrieving a dataset file."""
    file_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, "test.csv", sample_data)
    retrieved = dataset_file_storage.get_dataset(test_project_id, file_id)
    assert retrieved == sample_data


def test_check_dataset(dataset_file_storage, test_user_id, test_project_id, sample_data):
    """Test checking if a dataset file exists."""
    file_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, "test.csv", sample_data)
    assert dataset_file_storage.check_dataset(test_project_id, file_id) is True
    assert dataset_file_storage.check_dataset(test_project_id, "nonexistent") is False


def test_remove_dataset(dataset_file_storage, test_user_id, test_project_id, sample_data):
    """Test removing a dataset file."""
    file_id = dataset_file_storage.put_dataset(test_user_id, test_project_id, "test.csv", sample_data)
    assert dataset_file_storage.check_dataset(test_project_id, file_id) is True
    dataset_file_storage.remove_dataset(test_project_id, file_id)
    assert dataset_file_storage.check_dataset(test_project_id, file_id) is False


def test_get_dataset_blob_id(dataset_file_storage, test_project_id):
    """Test getting dataset blob ID."""
    blob_id = dataset_file_storage.get_dataset_blob_id(test_project_id, "test_file.csv")
    assert "datasets" in blob_id
    assert str(test_project_id) in blob_id
    assert "test_file.csv" in blob_id
