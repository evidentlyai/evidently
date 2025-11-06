from typing import Optional

try:
    from sqlalchemy import Engine
except ImportError as e:
    raise ImportError(
        "SQLAlchemy is required for SQL storage support. " "Please install it with: pip install evidently[sql]"
    ) from e

import logging

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
    "create_sql_project_manager",
]

from ...managers.auth import AuthManager
from ...managers.projects import ProjectManager
from ..common import NoopAuthManager

logger = logging.getLogger(__name__)


def create_engine_and_migrate(engine: Engine) -> Engine:
    # Run migrations on startup (fallback to create_all if migrations not initialized)
    try:
        migrate_database(str(engine.url))
    except (FileNotFoundError, ImportError):
        # Migrations not available - use create_all
        Base.metadata.create_all(engine)
    except Exception as e:
        # Check if it's because migrations aren't initialized (no alembic_version table)
        # In that case, fall back to create_all for backward compatibility
        from sqlalchemy import inspect

        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            # If alembic_version table doesn't exist, migrations aren't initialized
            if "alembic_version" not in tables:
                logger.debug(
                    "Migrations not initialized. Using create_all. "
                    "Initialize with: evidently migrate <url> --autogenerate -m 'initial'"
                )
                Base.metadata.create_all(engine)
            else:
                # Migrations are initialized but there's an error - re-raise it
                raise
        except Exception:
            # If we can't check (e.g., database doesn't exist yet), try create_all
            # This handles the case where we're creating a fresh database

            logger.debug(f"Could not run migrations: {e}. Falling back to create_all.")
            Base.metadata.create_all(engine)
    return engine


def create_sql_project_manager(engine: Engine, auth: Optional[AuthManager] = None) -> ProjectManager:
    engine = create_engine_and_migrate(engine)

    project_manager = ProjectManager(
        project_metadata=(SQLProjectMetadataStorage(engine)),
        blob_storage=SQLBlobStorage(engine),
        data_storage=(SQLDataStorage(engine)),
        auth_manager=auth or NoopAuthManager(),
        dashboard_manager=SQLDashboardManager(engine),
    )

    return project_manager


def migrate_database(database_url: str, revision: str = "head") -> None:
    """Run database migrations for SQL storage.

    This is a convenience function that can be called programmatically.
    For CLI usage, see: evidently migrate --help

    Args:
        database_url: Database connection URL (e.g., 'postgresql://user:pass@localhost/db')
        revision: Revision to upgrade to (default: 'head')
    """
    from evidently.cli.migrate import run_migrations

    run_migrations(database_url=database_url, revision=revision)
