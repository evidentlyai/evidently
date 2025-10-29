from typing import Optional

from sqlalchemy import create_engine

from .base import BaseSQLStorage
from .blob import SQLBlobStorage
from .components import SQLBlobComponent
from .components import SQLDataComponent
from .components import SQLMetadataComponent
from .dashboard import SQLDashboardManager
from .data import SQLDataStorage
from .metadata import SQLProjectMetadataStorage
from .models import Base

__all__ = [
    "BaseSQLStorage",
    "SQLBlobComponent",
    "SQLDataComponent",
    "SQLMetadataComponent",
    "SQLDashboardManager",
    "SQLDataStorage",
    "SQLProjectMetadataStorage",
    "Base",
]

from ...managers.auth import AuthManager
from ...managers.projects import ProjectManager
from ..common import NoopAuthManager


def create_sql_project_manager(url: str, auth: Optional[AuthManager] = None) -> ProjectManager:
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    project_manager = ProjectManager(
        project_metadata=(SQLProjectMetadataStorage(engine)),
        blob_storage=SQLBlobStorage(engine),
        data_storage=(SQLDataStorage(engine)),
        auth_manager=auth or NoopAuthManager(),
        dashboard_manager=SQLDashboardManager(engine),
    )

    return project_manager
