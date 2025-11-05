import posixpath
import time

from evidently.ui.service.storage.local.base import FSSpecBlobStorage
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

FileID = str


class FSSpecDatasetFileStorage(FSSpecBlobStorage):
    """File storage for dataset files."""

    @staticmethod
    def get_blob_name(user_id: UserID, filename: str) -> str:
        """Generate a unique blob name for a dataset file."""
        timestamp = int(time.time())
        paths = posixpath.split(filename)
        paths = paths[:-1] + (f"{user_id}-{timestamp}-{paths[-1]}",)
        return posixpath.sep.join(paths)

    @staticmethod
    def get_dataset_blob_id(project_id: ProjectID, file_id: FileID) -> str:
        """Get the blob ID for a dataset file."""
        return posixpath.join(str(project_id), "datasets", file_id)

    def put_bytes(self, path: str, obj: bytes) -> str:
        """Store bytes at the given path."""
        self.location.makedirs(posixpath.dirname(path))
        with self.location.open(path, "wb") as f:
            f.write(obj)
        return path

    def put_dataset(self, user_id: UserID, project_id: ProjectID, filename: str, data: bytes) -> FileID:
        """Store a dataset file and return its file ID."""
        file_id = self.get_blob_name(user_id, filename)
        path = self.get_dataset_blob_id(project_id, file_id)
        self.put_bytes(path, data)
        return file_id

    def get_bytes(self, path: str) -> bytes:
        """Retrieve bytes from the given path."""
        with self.location.open(path, "rb") as f:
            bytes_read = f.read()
        return bytes_read

    def get_dataset(self, project_id: ProjectID, file_id: FileID) -> bytes:
        """Retrieve a dataset file."""
        path = self.get_dataset_blob_id(project_id, file_id)
        return self.get_bytes(path)

    def check_dataset(self, project_id: ProjectID, file_id: FileID) -> bool:
        """Check if a dataset file exists."""
        path = self.get_dataset_blob_id(project_id, file_id)
        return self.location.exists(path)

    def remove_dataset(self, project_id: ProjectID, file_id: FileID) -> None:
        """Remove a dataset file."""
        path = self.get_dataset_blob_id(project_id, file_id)
        self.location.rmtree(path)
