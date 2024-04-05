from typing import Callable

from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import MetadataStorage
from evidently.ui.components.storage import BlobStorageComponent
from evidently.ui.components.storage import DataStorageComponent
from evidently.ui.components.storage import MetadataStorageComponent
from evidently.ui.storage.local import FSSpecBlobStorage
from evidently.ui.storage.local import InMemoryDataStorage
from evidently.ui.storage.local import JsonFileMetadataStorage


class FSSpecBlobComponent(BlobStorageComponent):
    class Config:
        type_alias = "fsspec"

    path: str

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        return lambda: FSSpecBlobStorage(base_path=self.path)


class JsonMetadataComponent(MetadataStorageComponent):
    class Config:
        type_alias = "json_file"

    path: str

    def dependency_factory(self) -> Callable[..., MetadataStorage]:
        return lambda: JsonFileMetadataStorage(path=self.path)


class InmemoryDataComponent(DataStorageComponent):
    class Config:
        type_alias = "d_inmemory"

    path: str

    def dependency_factory(self) -> Callable[..., DataStorage]:
        return lambda: InMemoryDataStorage(path=self.path)
