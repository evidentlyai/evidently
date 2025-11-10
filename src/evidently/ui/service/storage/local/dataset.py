import posixpath

from evidently.legacy.utils.sync import async_to_sync
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.managers.base import BaseDependant
from evidently.ui.service.type_aliases import BlobID
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

FileID = str


class DatasetFileStorage(BaseDependant):
    dataset_blob_storage: BlobStorage

    @staticmethod
    def get_dataset_blob_id(project_id: ProjectID, dataset_id: DatasetID, filename: str) -> str:
        """Get the blob ID for a dataset file."""
        return posixpath.join(str(project_id), "datasets", str(dataset_id), filename)

    def put_dataset(
        self, user_id: UserID, project_id: ProjectID, dataset_id: DatasetID, filename: str, file_content: bytes
    ):
        blob_id = self.get_dataset_blob_id(project_id, dataset_id, filename)

        async_to_sync(self.dataset_blob_storage.put_blob(blob_id, file_content))
        return blob_id

    def get_dataset(self, blob_id: BlobID) -> bytes:
        """Retrieve a dataset file."""
        return self.dataset_blob_storage.get_blob_data(blob_id)

    def check_dataset(self, blob_id: BlobID) -> bool:
        """Check if a dataset file exists."""
        return self.dataset_blob_storage.blob_exists(blob_id)

    def remove_dataset(self, blob_id: BlobID) -> None:
        """Remove a dataset file."""
        async_to_sync(self.dataset_blob_storage.delete_blob(blob_id))
