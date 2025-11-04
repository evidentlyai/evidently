import pathlib
from typing import Optional

from typer import Argument
from typer import Option
from typer import echo

from evidently.cli.main import app


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
    try:
        from alembic import command
        from alembic.config import Config
    except ImportError as e:
        raise ImportError(
            "Alembic is required for migrations. Please install it with: pip install evidently[sql]"
        ) from e

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
            raise ValueError("--message is required when using --autogenerate")
        echo(f"Creating new migration: {message}")
        command.revision(config, autogenerate=True, message=message)
        echo("Migration file created. Please review it before applying.")
    elif downgrade:
        echo(f"Downgrading to revision: {revision}")
        command.downgrade(config, revision)
        echo("Downgrade complete.")
    else:
        echo(f"Upgrading to revision: {revision}")
        command.upgrade(config, revision)
        echo("Upgrade complete.")


@app.command("migrate")
def migrate(
    database_url: str = Argument(..., help="Database connection URL (e.g., 'postgresql://user:pass@localhost/db')"),
    revision: str = Option("head", help="Revision to upgrade/downgrade to"),
    downgrade: bool = Option(False, "--downgrade", "-d", help="Downgrade instead of upgrade"),
    autogenerate: bool = Option(False, "--autogenerate", "-a", help="Create new migration from model changes"),
    message: Optional[str] = Option(
        None, "--message", "-m", help="Message for new migration (required with --autogenerate)"
    ),
):
    """Run database migrations for SQL storage.

    Examples:
        # Upgrade to latest migration
        evidently migrate postgresql://user:pass@localhost/evidently

        # Upgrade to specific revision
        evidently migrate postgresql://user:pass@localhost/evidently --revision abc123

        # Create new migration from model changes
        evidently migrate postgresql://user:pass@localhost/evidently --autogenerate -m "add new column"

        # Downgrade one revision
        evidently migrate postgresql://user:pass@localhost/evidently --downgrade --revision -1
    """
    run_migrations(
        database_url=database_url, revision=revision, downgrade=downgrade, autogenerate=autogenerate, message=message
    )


@app.command("migrate-status")
def migrate_status(
    database_url: str = Argument(..., help="Database connection URL"),
):
    """Check current migration status."""
    try:
        from alembic import command
        from alembic.config import Config
    except ImportError as e:
        raise ImportError(
            "Alembic is required for migrations. Please install it with: pip install evidently[sql]"
        ) from e

    import evidently.ui.service.storage.sql.migrations

    migrations_dir = pathlib.Path(evidently.ui.service.storage.sql.migrations.__file__).parent
    alembic_ini = migrations_dir / "alembic.ini"

    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)
    config.set_section_option("alembic", "script_location", str(migrations_dir))
    # Add the evidently src directory to sys.path so imports work
    import evidently

    evidently_src = pathlib.Path(evidently.__file__).parent.parent
    config.set_section_option("alembic", "prepend_sys_path", str(evidently_src))

    echo("Current database revision:")
    command.current(config, verbose=True)

    echo("\nMigration history:")
    command.history(config, verbose=True)
