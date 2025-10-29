from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional

from sqlalchemy import Engine
from sqlalchemy import create_engine

from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import DataStorageComponent
from evidently.ui.service.components.storage import MetadataStorageComponent
from evidently.ui.service.storage.sql.blob import SQLBlobStorage
from evidently.ui.service.storage.sql.data import SQLDataStorage
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage


class SQLEngineComponent(FactoryComponent[Engine]):
    """Component for providing SQLAlchemy engine."""

    class Config:
        is_base_type = True

    __section__: ClassVar = "database"
    dependency_name: ClassVar = "engine"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = True

    def dependency_factory(self) -> Callable[..., Engine]:
        """Create engine factory."""
        raise NotImplementedError


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


class DatabaseComponent(SQLEngineComponent):
    """Database component with connection parameters."""

    class Config:
        type_alias = "database"

    type_: str
    host: str
    port: Optional[int] = None
    database: str
    username: str
    password: str
    params: dict = {}

    def dependency_factory(self) -> Callable[..., Engine]:
        """Create database engine factory."""

        def create_engine_factory() -> Engine:
            conn_args: Dict[str, Any] = {
                "host": self.host,
                "user": self.username,
                "password": self.password,
                "dbname": self.database,
                **self.params,
            }
            if self.port is not None:
                conn_args["port"] = self.port

            engine = create_engine(f"{self.type_}://", connect_args=conn_args)
            return engine

        return create_engine_factory


class SimpleDatabaseComponent(SQLEngineComponent):
    """Simple database component with connection URL."""

    class Config:
        type_alias = "simple"

    url: str
    create_all: bool = False

    def dependency_factory(self) -> Callable[..., Engine]:
        """Create simple database engine factory."""

        def create_engine_factory() -> Engine:
            engine = create_engine(self.url)
            if self.create_all:
                from evidently.ui.service.storage.sql.models import Base
                from evidently.ui.service.storage.sql.models import PostgresSQLBase
                from evidently.ui.service.storage.sql.models import SQLiteBase

                Base.metadata.create_all(engine)
                if engine.dialect.name == "sqlite":
                    SQLiteBase.metadata.create_all(engine)
                if engine.dialect.name.startswith("postgresql"):
                    PostgresSQLBase.metadata.create_all(engine)
            return engine

        return create_engine_factory
