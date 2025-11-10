from io import BytesIO

import pandas as pd
import pytest
from litestar.exceptions import HTTPException

from evidently.legacy.core import new_id
from evidently.ui.service.datasets.file_io import FileIO
from evidently.ui.service.datasets.file_io import get_upload_file
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
def file_io(dataset_file_storage):
    """Create FileIO instance."""
    return FileIO(dataset_file_storage)


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
def sample_csv_data():
    """Create sample CSV data."""
    return b"col1,col2\n1,a\n2,b\n3,c"


@pytest.fixture
def sample_parquet_data(sample_dataframe):
    """Create sample parquet data."""
    buf = BytesIO()
    sample_dataframe.to_parquet(buf, engine="pyarrow")
    return buf.getvalue()


def test_read_file_from_storage_csv(file_io, test_user_id, test_project_id, test_dataset_id, sample_csv_data):
    """Test reading CSV file from storage."""
    blob_id = file_io.file_storage.put_dataset(
        test_user_id, test_project_id, test_dataset_id, "test.csv", sample_csv_data
    )
    df = file_io.read_file_from_storage(test_project_id, blob_id)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[0]["col2"] == "a"


def test_read_file_from_storage_parquet(file_io, test_user_id, test_project_id, test_dataset_id, sample_parquet_data):
    """Test reading parquet file from storage."""
    blob_id = file_io.file_storage.put_dataset(
        test_user_id, test_project_id, test_dataset_id, "test.parquet", sample_parquet_data
    )
    df = file_io.read_file_from_storage(test_project_id, blob_id)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[0]["col2"] == "a"


def test_read_file_from_storage_invalid_extension(file_io, test_user_id, test_project_id, test_dataset_id):
    """Test reading file with invalid extension."""
    blob_id = file_io.file_storage.put_dataset(test_user_id, test_project_id, test_dataset_id, "test.txt", b"some data")
    with pytest.raises(HTTPException) as exc_info:
        file_io.read_file_from_storage(test_project_id, blob_id)
    assert exc_info.value.status_code == 400
    assert "Extension not allowed" in exc_info.value.detail


def test_read_file_from_storage_missing_file(file_io, test_project_id):
    """Test reading non-existent file."""
    with pytest.raises(Exception):
        file_io.read_file_from_storage(test_project_id, "nonexistent/file/id.parquet")


def test_get_upload_file(sample_dataframe):
    """Test creating UploadFile from dataframe."""
    upload_file = get_upload_file(sample_dataframe, "test_dataset")
    assert upload_file.filename == "test_dataset.parquet"
    assert upload_file.content_type == "application/octet-stream"

    # Read file content
    upload_file.file.seek(0)
    file_content = upload_file.file.read()
    assert len(file_content) > 0

    # Verify we can read it back
    df = pd.read_parquet(BytesIO(file_content), engine="pyarrow")
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1


def test_get_upload_file_empty_dataframe():
    """Test creating UploadFile from empty dataframe."""
    empty_df = pd.DataFrame()
    upload_file = get_upload_file(empty_df, "empty")
    assert upload_file.filename == "empty.parquet"
    upload_file.file.seek(0)
    file_content = upload_file.file.read()
    df = pd.read_parquet(BytesIO(file_content), engine="pyarrow")
    assert len(df) == 0
