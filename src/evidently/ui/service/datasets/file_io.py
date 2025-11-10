import os
from io import BytesIO
from typing import Callable
from typing import Container
from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd
from litestar.datastructures import UploadFile
from litestar.exceptions import HTTPException
from pandas.errors import ParserError

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.legacy.ui.type_aliases import UserID
from evidently.ui.service.storage.local.dataset import DatasetFileStorage
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID

FileID = str


class FileData:
    """Data structure for file upload result."""

    def __init__(
        self,
        filename: str,
        columns: List[str],
        data_definition: DataDefinition,
        size_bytes: int,
        row_count: int,
        column_count: int,
    ):
        self.filename = filename
        self.columns = columns
        self.data_definition = data_definition
        self.size_bytes = size_bytes
        self.row_count = row_count
        self.column_count = column_count


def calculate_data_definition(current_data: pd.DataFrame) -> DataDefinition:
    """Calculate data definition from a dataframe."""
    dataset = Dataset.from_pandas(current_data)
    return dataset.data_definition


def read_parquet(path) -> pd.DataFrame:
    """Read parquet file."""
    df = pd.read_parquet(path, engine="pyarrow")
    return df


class FileIO:
    """Utility for reading and writing dataset files."""

    def __init__(self, file_storage: DatasetFileStorage):
        self.file_storage = file_storage

    ALLOWED_FILE_READERS = {
        ".csv": pd.read_csv,
        ".parquet": read_parquet,
    }

    def save_file(
        self,
        user_id: UserID,
        project_id: ProjectID,
        dataset_id: DatasetID,
        upload_file: UploadFile,
        allowed_extensions: Optional[Container[str]] = None,
    ) -> Tuple[FileID, str, bytes]:
        """Save an uploaded file and return file ID, extension, and content."""
        _, file_extension = os.path.splitext(upload_file.filename)
        if allowed_extensions is not None and file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Extension not allowed")
        file_content: bytes = upload_file.file.read()
        return (
            self.file_storage.put_dataset(user_id, project_id, dataset_id, upload_file.filename, file_content),
            file_extension,
            file_content,
        )

    def save_dataframe(
        self, user_id: UserID, project_id: ProjectID, dataset_id: DatasetID, upload_file: UploadFile
    ) -> Tuple[str, pd.DataFrame, int]:
        """Save uploaded file as dataframe."""
        file_id, file_extension, file_content = self.save_file(
            user_id, project_id, dataset_id, upload_file, allowed_extensions=self.ALLOWED_FILE_READERS.keys()
        )
        try:
            reader: Callable[[BytesIO], pd.DataFrame] = self.ALLOWED_FILE_READERS[file_extension]  # type: ignore[assignment]
            current_data = reader(BytesIO(file_content))
        except ParserError as e:
            raise HTTPException(status_code=400, detail=f"Wrong file content: {str(e)}")
        return file_id, current_data, int(len(file_content))

    def save_dataframe_and_calculate_data_definition(
        self,
        user_id: UserID,
        project_id: ProjectID,
        dataset_id: DatasetID,
        file: UploadFile,
        data_definition: Optional[DataDefinition] = None,
    ) -> FileData:
        """Save dataframe and calculate data definition."""
        file_id, current_data, size_bytes = self.save_dataframe(user_id, project_id, dataset_id, file)
        result_dd = data_definition
        if data_definition is None:
            try:
                result_dd = calculate_data_definition(current_data)
            except Exception as e:
                self.file_storage.remove_dataset(file_id)
                raise e

        if result_dd is None:
            raise ValueError("Data definition is required")

        row_count, column_count = current_data.shape

        return FileData(
            filename=file_id,
            data_definition=result_dd,
            columns=list(current_data.columns),
            size_bytes=size_bytes,
            row_count=row_count,
            column_count=column_count,
        )

    def read_file_from_storage(
        self,
        project_id: ProjectID,
        file_id: str,
    ) -> pd.DataFrame:
        """Read a file from storage."""
        _, file_extension = os.path.splitext(file_id)
        if file_extension not in self.ALLOWED_FILE_READERS.keys():
            raise HTTPException(status_code=400, detail="Extension not allowed")
        file_content = self.file_storage.get_dataset(file_id)
        reader: Callable[[BytesIO], pd.DataFrame] = self.ALLOWED_FILE_READERS[file_extension]  # type: ignore[assignment]
        df = reader(BytesIO(file_content))
        return df


def get_upload_file(df: pd.DataFrame, name: str) -> UploadFile:
    """Create an UploadFile from a dataframe."""
    from io import BytesIO

    buf = BytesIO()
    df.to_parquet(buf)
    buf.seek(0)
    return UploadFile(
        content_type="application/octet-stream",
        filename=f"{name}.parquet",
        file_data=buf.getvalue(),
    )
