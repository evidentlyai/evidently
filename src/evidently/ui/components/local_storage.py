from typing import Callable
from typing import ClassVar
from typing import Optional

from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import ProjectMetadataStorage
from evidently.ui.components.base import FactoryComponent
from evidently.ui.components.storage import BlobStorageComponent
from evidently.ui.components.storage import DataStorageComponent
from evidently.ui.components.storage import MetadataStorageComponent
from evidently.ui.storage.local import FSSpecBlobStorage
from evidently.ui.storage.local import InMemoryDataStorage
from evidently.ui.storage.local import JsonFileProjectMetadataStorage
from evidently.ui.storage.local import LocalState


class FSSpecBlobComponent(BlobStorageComponent):
    __type_alias__: ClassVar = "fsspec"

    path: str

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        return lambda: FSSpecBlobStorage(base_path=self.path)


class JsonMetadataComponent(MetadataStorageComponent):
    __type_alias__: ClassVar = "json_file"

    path: str

    def dependency_factory(self) -> Callable[..., ProjectMetadataStorage]:
        async def json_meta(local_state: Optional[LocalState] = None):
            return JsonFileProjectMetadataStorage(path=self.path, local_state=local_state)

        return json_meta  # type: ignore[return-value]


class InmemoryDataComponent(DataStorageComponent):
    __type_alias__: ClassVar = "inmemory"

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
