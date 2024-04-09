from abc import ABC
from typing import Callable
from typing import ClassVar

from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import MetadataStorage
from evidently.ui.base import ProjectManager
from evidently.ui.components.base import FactoryComponent
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.storage.local import create_local_project_manager


class StorageComponent(FactoryComponent[ProjectManager], ABC):
    dependency_name: ClassVar = "project_manager"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = True


class LocalStorageComponent(StorageComponent):
    path: str = "workspace"
    autorefresh: bool = True

    def dependency_factory(self) -> Callable[..., ProjectManager]:
        return lambda: create_local_project_manager(self.path, autorefresh=self.autorefresh, auth=NoopAuthManager())


class MetadataStorageComponent(FactoryComponent[MetadataStorage], ABC):
    __section__: ClassVar = "metadata"
    dependency_name: ClassVar = "metadata_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class DataStorageComponent(FactoryComponent[DataStorage], ABC):
    __section__: ClassVar = "data"

    dependency_name: ClassVar = "data_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class BlobStorageComponent(FactoryComponent[BlobStorage], ABC):
    __section__: ClassVar = "blob"

    dependency_name: ClassVar = "blob_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False
