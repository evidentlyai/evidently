from typing import Callable
from typing import ClassVar
from typing import Optional

from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.components.snapshot_links import SnapshotDatasetLinksComponent
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import DatasetFileStorageComponent
from evidently.ui.service.components.storage import DatasetMetadataComponent
from evidently.ui.service.components.storage import DataStorageComponent
from evidently.ui.service.components.storage import MetadataStorageComponent
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.metadata import FileDatasetMetadataStorage
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.storage.local import FSSpecBlobStorage
from evidently.ui.service.storage.local import InMemoryDataStorage
from evidently.ui.service.storage.local import JsonFileProjectMetadataStorage
from evidently.ui.service.storage.local import LocalState
from evidently.ui.service.storage.local.snapshot_links import FileSnapshotDatasetLinksManager


class FSSpecBlobComponent(BlobStorageComponent):
    class Config:
        type_alias = "fsspec"

    path: str

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        def blob_storage_factory() -> BlobStorage:
            return FSSpecBlobStorage(base_path=self.path)

        return blob_storage_factory


class JsonMetadataComponent(MetadataStorageComponent):
    class Config:
        type_alias = "json_file"

    path: str

    def dependency_factory(self) -> Callable[..., ProjectMetadataStorage]:
        async def json_meta(local_state: Optional[LocalState] = None):
            return JsonFileProjectMetadataStorage(path=self.path, local_state=local_state)

        return json_meta  # type: ignore[return-value]


class InmemoryDataComponent(DataStorageComponent):
    class Config:
        type_alias = "inmemory"

    path: str

    def dependency_factory(self) -> Callable[..., DataStorage]:
        def inmemory_data(local_state: Optional[LocalState] = None):
            return InMemoryDataStorage(path=self.path, local_state=local_state)

        return inmemory_data


class LocalStateComponent(FactoryComponent[LocalState]):
    __section__: ClassVar = "local_state"
    dependency_name: ClassVar = "local_state"

    path: str

    def dependency_factory(self) -> Callable[..., LocalState]:
        return lambda: LocalState(path=self.path, project_manager=None)


class JsonDatasetMetadataComponent(DatasetMetadataComponent):
    """JSON file-based dataset metadata storage component."""

    class Config:
        type_alias = "json_file"

    path: str = "workspace"

    def dependency_factory(self) -> Callable[..., DatasetMetadataStorage]:
        def dataset_metadata_factory() -> DatasetMetadataStorage:
            return FileDatasetMetadataStorage(base_path=self.path)

        return dataset_metadata_factory


class FSSpecDatasetFileStorageComponent(DatasetFileStorageComponent):
    """FSSpec-based dataset file storage component."""

    class Config:
        type_alias = "fsspec"

    path: str = "workspace"

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        def blob_storage_factory() -> BlobStorage:
            return FSSpecBlobStorage(base_path=self.path)

        return blob_storage_factory


class FileSnapshotDatasetLinksComponent(SnapshotDatasetLinksComponent):
    """File-based snapshot dataset links component."""

    class Config:
        type_alias = "file"

    path: str = "workspace"

    def dependency_factory(self) -> Callable[..., SnapshotDatasetLinksManager]:
        def snapshot_dataset_links_factory() -> SnapshotDatasetLinksManager:
            return FileSnapshotDatasetLinksManager(base_path=self.path)

        return snapshot_dataset_links_factory
