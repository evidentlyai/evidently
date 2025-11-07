from abc import ABC
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional

from litestar.di import Provide
from sqlalchemy import Engine
from sqlalchemy import create_engine

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import SecretStr
from evidently.legacy.utils.numpy_encoder import numpy_dumps
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.components.snapshot_links import SnapshotDatasetLinksComponent
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import DatasetFileStorageComponent
from evidently.ui.service.components.storage import DatasetMetadataComponent
from evidently.ui.service.components.storage import DataStorageComponent
from evidently.ui.service.components.storage import MetadataStorageComponent
from evidently.ui.service.components.storage import StorageComponent
from evidently.ui.service.datasets.metadata import DatasetMetadataStorage
from evidently.ui.service.datasets.snapshot_links import SnapshotDatasetLinksManager
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.storage.common import NoopAuthManager
from evidently.ui.service.storage.sql.blob import SQLBlobStorage
from evidently.ui.service.storage.sql.data import SQLDataStorage
from evidently.ui.service.storage.sql.dataset import SQLDatasetMetadataStorage
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage
from evidently.ui.service.storage.sql.snapshot_links import SQLSnapshotDatasetLinksManager
from evidently.ui.service.storage.sql.utils import create_sql_project_manager


class SQLMetadataComponent(MetadataStorageComponent):
    """SQL metadata storage component."""

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., ProjectMetadataStorage]:
        """Create SQL metadata storage factory."""
        return SQLProjectMetadataStorage


class SQLDataComponent(DataStorageComponent):
    """SQL data storage component."""

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., DataStorage]:
        """Create SQL data storage factory."""

        def sql_data_storage(engine: Engine) -> SQLDataStorage:
            return SQLDataStorage(engine=engine)

        return sql_data_storage


class SQLBlobComponent(BlobStorageComponent):
    """SQL blob storage component."""

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        """Create SQL blob storage factory."""

        def sql_blob_storage(engine: Engine) -> SQLBlobStorage:
            return SQLBlobStorage(engine=engine)

        return sql_blob_storage


class DatabaseConfig(BaseModel):
    type_: str
    host: str
    port: Optional[int] = None
    database: str
    username: str
    password: SecretStr
    params: Dict[str, str] = Field(default_factory=dict)

    def get_engine(self) -> Engine:
        conn_args: Dict[str, Any] = {
            "host": self.host,
            "user": self.username,
            "password": self.password.get_secret_value(),
            "dbname": self.database,
            **self.params,
        }
        if self.port is not None:
            conn_args["port"] = self.port

        engine = create_engine(f"{self.type_}://", connect_args=conn_args or {}, json_serializer=numpy_dumps)
        return engine


class DatabaseComponent(Component, ABC):
    __section__: ClassVar = "database"

    url: Optional[str] = None
    config: Optional[DatabaseConfig] = None

    def get_engine(self) -> Engine:
        if self.url is None and self.config is None:
            raise ValueError("You must specify either url or config")
        if self.url is not None and self.config is not None:
            raise ValueError("You cannot specify both url or config")
        if self.url is not None:
            return create_engine(self.url, json_serializer=numpy_dumps)
        if self.config is None:
            raise ValueError("Config is required when url is not provided")
        return self.config.get_engine()

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {"engine": Provide(self.get_engine, sync_to_thread=True, use_cache=True)}


class SQLStorageComponent(StorageComponent):
    __require__: ClassVar = [DatabaseComponent]

    class Config:
        type_alias = "sql"

    def project_manager_provider(self) -> Callable[..., Awaitable[ProjectManager]]:
        async def project_manager_factory(engine: Engine) -> ProjectManager:
            return create_sql_project_manager(engine, auth=NoopAuthManager())

        return project_manager_factory

    def dataset_blob_storage_provider(self) -> Callable[..., Awaitable[BlobStorage]]:
        async def dataset_blob_storage_factory(engine: Engine) -> SQLBlobStorage:
            return SQLBlobStorage(engine=engine)

        return dataset_blob_storage_factory

    def dataset_metadata_provider(self) -> Callable[..., Awaitable[DatasetMetadataStorage]]:
        async def dataset_metadata_factory(engine: Engine) -> DatasetMetadataStorage:
            return SQLDatasetMetadataStorage(engine=engine)

        return dataset_metadata_factory

    def snapshot_dataset_links_provider(self) -> Callable[..., Awaitable[SnapshotDatasetLinksManager]]:
        async def snapshot_dataset_links_factory(engine: Engine) -> SnapshotDatasetLinksManager:
            return SQLSnapshotDatasetLinksManager(engine=engine)

        return snapshot_dataset_links_factory


class SQLDatasetMetadataComponent(DatasetMetadataComponent):
    """SQL-based dataset metadata storage component."""

    __require__: ClassVar = [DatabaseComponent]

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., DatasetMetadataStorage]:
        def sql_dataset_metadata(engine: Engine) -> DatasetMetadataStorage:
            return SQLDatasetMetadataStorage(engine=engine)

        return sql_dataset_metadata


class SQLDatasetFileStorageComponent(DatasetFileStorageComponent):
    """SQL-based dataset file storage component."""

    __require__: ClassVar = [DatabaseComponent]

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., BlobStorage]:
        def sql_dataset_file_storage(engine: Engine) -> BlobStorage:
            return SQLBlobStorage(engine=engine)

        return sql_dataset_file_storage


class SQLSnapshotDatasetLinksComponent(SnapshotDatasetLinksComponent):
    """SQL-based snapshot dataset links component."""

    __require__: ClassVar = [DatabaseComponent]

    class Config:
        type_alias = "sql"

    def dependency_factory(self) -> Callable[..., SnapshotDatasetLinksManager]:
        def sql_snapshot_dataset_links(engine: Engine) -> SnapshotDatasetLinksManager:
            return SQLSnapshotDatasetLinksManager(engine=engine)

        return sql_snapshot_dataset_links
