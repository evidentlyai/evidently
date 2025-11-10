import logging
import pathlib
from typing import Optional

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine

from ...managers.auth import AuthManager
from ...managers.projects import ProjectManager
from ..common import NoopAuthManager
from .blob import SQLBlobStorage
from .dashboard import SQLDashboardManager
from .data import SQLDataStorage
from .metadata import SQLProjectMetadataStorage
from .models import Base

logger = logging.getLogger(__name__)


def create_engine_and_migrate(engine: Engine) -> Engine:
    # Run migrations on startup (fallback to create_all if migrations not initialized)
    try:
        logger.info("Running database migrations...")
        migrate_database(str(engine.url))
        logger.info("Database migrations completed successfully")
    except (FileNotFoundError, ImportError):
        # Migrations not available - use create_all
        logger.debug("Migrations not available, using create_all")
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
                logger.error(f"Migration error: {e}", exc_info=True)
                raise
        except Exception:
            # If we can't check (e.g., database doesn't exist yet), try create_all
            # This handles the case where we're creating a fresh database

            logger.debug(f"Could not run migrations: {e}. Falling back to create_all.")
            Base.metadata.create_all(engine)
    return engine


def create_sql_project_manager(engine: Engine, auth: Optional[AuthManager] = None) -> ProjectManager:
    engine = create_engine_and_migrate(engine)

    blob_storage = SQLBlobStorage(engine)
    metadata_storage = SQLProjectMetadataStorage(engine)
    data_storage = SQLDataStorage(engine)
    project_manager = ProjectManager(
        project_metadata=metadata_storage,
        blob_storage=blob_storage,
        data_storage=data_storage,
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

    run_migrations(database_url=database_url, revision=revision)


def run_migrations(
    database_url: str,
    revision: str = "head",
    downgrade: bool = False,
    autogenerate: bool = False,
    message: Optional[str] = None,
) -> None:
    """Run Alembic migrations for SQL storage.

    Args:
        database_url: Database connection URL (e.g., 'postgresql://user:pass@localhost/db')
        revision: Revision to upgrade/downgrade to (default: 'head')
        downgrade: If True, downgrade instead of upgrade
        autogenerate: If True, create a new migration from model changes
        message: Message for new migration (required if autogenerate=True)
    """

    # Get the migrations directory path
    import evidently.ui.service.storage.sql.migrations

    migrations_dir = pathlib.Path(evidently.ui.service.storage.sql.migrations.__file__).parent
    alembic_ini = migrations_dir / "alembic.ini"

    if not alembic_ini.exists():
        raise FileNotFoundError(f"Could not find alembic.ini at {alembic_ini}")

    # Create Alembic config - pass alembic.ini path and it will be used as the base directory
    # When we change the script_location, we need to use an absolute path
    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)

    # Set script location to the migrations directory (absolute path)
    config.set_section_option("alembic", "script_location", str(migrations_dir))
    # Add the evidently src directory to sys.path so imports work
    import evidently

    evidently_src = pathlib.Path(evidently.__file__).parent.parent
    config.set_section_option("alembic", "prepend_sys_path", str(evidently_src))

    if autogenerate:
        if not message:
            raise ValueError("message is required when using autogenerate")
        command.revision(config, autogenerate=True, message=message)
    elif downgrade:
        command.downgrade(config, revision)
    else:
        command.upgrade(config, revision)
