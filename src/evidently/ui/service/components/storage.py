from abc import ABC
from typing import Callable
from typing import ClassVar
from typing import Optional

from evidently.pydantic_utils import register_type_alias
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.storage.common import NoopAuthManager
from evidently.ui.service.storage.local import create_local_project_manager


class StorageComponent(FactoryComponent[ProjectManager], ABC):
    class Config:
        is_base_type = True

    dependency_name: ClassVar = "project_manager"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class LocalStorageComponent(StorageComponent):
    path: str = "workspace"
    autorefresh: bool = True

    def dependency_factory(self) -> Callable[..., ProjectManager]:
        return lambda: create_local_project_manager(self.path, autorefresh=self.autorefresh, auth=NoopAuthManager())


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


register_type_alias(BlobStorageComponent, "evidently.ui.service.components.local_storage.FSSpecBlobComponent", "fsspec")
register_type_alias(
    MetadataStorageComponent, "evidently.ui.service.components.local_storage.JsonMetadataComponent", "json_file"
)
register_type_alias(
    DataStorageComponent, "evidently.ui.service.components.local_storage.InmemoryDataComponent", "inmemory"
)
