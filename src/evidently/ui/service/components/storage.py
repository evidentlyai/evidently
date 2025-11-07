from abc import ABC
from abc import abstractmethod
from typing import Awaitable
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional

from litestar.di import Provide

from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.components.snapshot_links import SnapshotDatasetLinksComponent
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.metadata import FileDatasetMetadataStorage
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.storage.common import NoopAuthManager
from evidently.ui.service.storage.local import FSSpecBlobStorage
from evidently.ui.service.storage.local import create_local_project_manager
from evidently.ui.service.storage.local.snapshot_links import FileSnapshotDatasetLinksManager


class DatasetMetadataComponent(FactoryComponent[DatasetMetadataStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar[str] = "dataset_metadata"
    dependency_name: ClassVar[str] = "dataset_metadata"
    use_cache: ClassVar[bool] = True

    def dependency_factory(self) -> Callable[..., DatasetMetadataStorage]:
        raise NotImplementedError(self.__class__)


class DatasetFileStorageComponent(FactoryComponent[BlobStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar[str] = "dataset_storage"
    dependency_name: ClassVar[str] = "dataset_blob_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        raise NotImplementedError(self.__class__)


class StorageComponent(Component, ABC):
    class Config:
        is_base_type = True

    dependency_name: ClassVar = "project_manager"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        deps = {
            "project_manager": Provide(self.project_manager_provider(), use_cache=self.use_cache),
        }
        # if no components configured, use default
        if ctx.get_component(DatasetMetadataComponent, required=False) is None:
            deps["dataset_metadata"] = Provide(self.dataset_metadata_provider(), use_cache=self.use_cache)
        if ctx.get_component(DatasetFileStorageComponent, required=False) is None:
            deps["dataset_blob_storage"] = Provide(self.dataset_blob_storage_provider(), use_cache=self.use_cache)
        if ctx.get_component(SnapshotDatasetLinksComponent, required=False) is None:
            deps["snapshot_dataset_links"] = Provide(self.snapshot_dataset_links_provider(), use_cache=self.use_cache)
        # todo: same for project_manager dependencies
        return deps

    @abstractmethod
    def project_manager_provider(self) -> Callable[..., Awaitable[ProjectManager]]:
        raise NotImplementedError(f"{self.__class__.__name__}")

    def dataset_blob_storage_provider(self) -> Callable[..., Awaitable[BlobStorage]]:
        raise NotImplementedError(f"{self.__class__.__name__} does not have default dataset_file_storage provider")

    def dataset_metadata_provider(self) -> Callable[..., Awaitable[DatasetMetadataStorage]]:
        raise NotImplementedError(f"{self.__class__.__name__} does not have default dataset_metadata provider")

    def snapshot_dataset_links_provider(self) -> Callable[..., Awaitable[SnapshotDatasetLinksManager]]:
        raise NotImplementedError(f"{self.__class__.__name__} does not have default snapshot_dataset_links provider")


class LocalStorageComponent(StorageComponent):
    class Config:
        type_alias = "local"

    path: str = "workspace"
    autorefresh: bool = True

    def project_manager_provider(self):
        async def project_manager_factory() -> ProjectManager:
            return create_local_project_manager(self.path, autorefresh=self.autorefresh, auth=NoopAuthManager())

        return project_manager_factory

    def dataset_blob_storage_provider(self):
        async def dataset_blob_storage_factory() -> BlobStorage:
            return FSSpecBlobStorage(base_path=self.path)

        return dataset_blob_storage_factory

    def dataset_metadata_provider(self):
        async def dataset_metadata_factory() -> DatasetMetadataStorage:
            return FileDatasetMetadataStorage(base_path=self.path)

        return dataset_metadata_factory

    def snapshot_dataset_links_provider(self):
        async def snapshot_dataset_links_factory() -> SnapshotDatasetLinksManager:
            return FileSnapshotDatasetLinksManager(base_path=self.path)

        return snapshot_dataset_links_factory


class MetadataStorageComponent(FactoryComponent[ProjectMetadataStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "metadata"
    dependency_name: ClassVar = "project_metadata"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[Optional[bool]] = None


class DataStorageComponent(FactoryComponent[DataStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "data"

    dependency_name: ClassVar = "data_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class BlobStorageComponent(FactoryComponent[BlobStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "blob"

    dependency_name: ClassVar = "blob_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False
