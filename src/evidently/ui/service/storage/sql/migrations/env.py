from logging.config import fileConfig

from alembic import context

# Import all models so Alembic can detect them
from evidently.ui.service.storage.sql.models import Base  # noqa: F401
from evidently.ui.service.storage.sql.models import BlobSQLModel  # noqa: F401
from evidently.ui.service.storage.sql.models import MetricsSQLModel  # noqa: F401
from evidently.ui.service.storage.sql.models import PointSQLModel  # noqa: F401
from evidently.ui.service.storage.sql.models import ProjectSQLModel  # noqa: F401
from evidently.ui.service.storage.sql.models import SnapshotSQLModel  # noqa: F401
from evidently.ui.service.storage.sql.models import UserSQLModel  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# Use getattr to safely access config - it may not be available during import
config = getattr(context, "config", None)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# Only configure logging when running via Alembic CLI (not programmatically)
# This prevents overriding the application's logging configuration when migrations
# are run from within the application (e.g., on startup)
if config is not None and config.config_file_name is not None:
    # Check if we're being called from Alembic CLI vs programmatically
    # When called programmatically (e.g., via migrate_database), we don't want
    # to override the application's logging configuration
    import os
    import sys

    # Only configure logging if:
    # 1. Running via Alembic CLI (alembic command in argv[0])
    # 2. Or explicitly set via environment variable
    is_alembic_cli = (
        "alembic" in sys.argv[0]
        or os.path.basename(sys.argv[0]) == "alembic"
        or any("alembic" in arg for arg in sys.argv)
    )

    # Don't configure logging when called programmatically to avoid overriding app logging
    if is_alembic_cli:
        fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get config from context (it should be available when Alembic runs this)
    config = context.config
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise ValueError("sqlalchemy.url must be set in alembic.ini or provided via -x url=<database_url>")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get config from context (it should be available when Alembic runs this)
    config = context.config
    # Check if a connection/engine was provided via config attributes
    connectable = config.attributes.get("connection", None)

    if connectable is None:
        # Check if URL was provided via -x url argument
        url = context.get_x_argument(as_dictionary=True).get("url", None)
        if url:
            from sqlalchemy import create_engine

            connectable = create_engine(url)
        else:
            # Try to get URL from config
            url = config.get_main_option("sqlalchemy.url")
            if url:
                from sqlalchemy import create_engine

                connectable = create_engine(url)
            else:
                raise ValueError(
                    "Database connection required. Provide via: "
                    "-x url=<database_url> or set sqlalchemy.url in alembic.ini"
                )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Only run migrations when Alembic executes this script
# (not when the module is imported)
if hasattr(context, "config"):
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
