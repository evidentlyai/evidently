from typing import Callable

from sqlalchemy import Engine

from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import DataStorageComponent
from evidently.ui.service.components.storage import MetadataStorageComponent
from evidently.ui.service.storage.sql.blob import SQLBlobStorage
from evidently.ui.service.storage.sql.data import SQLDataStorage
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage


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
