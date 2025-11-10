import tempfile

import pytest
from sqlalchemy import create_engine

from evidently.legacy.core import new_id
from evidently.ui.service.base import Project
from evidently.ui.service.base import User
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage
from evidently.ui.service.storage.sql.utils import migrate_database
from evidently.ui.service.type_aliases import ZERO_UUID


@pytest.fixture
def sqlite_engine():
    """Create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    engine = create_engine(f"sqlite:///{db_path}")
    migrate_database(f"sqlite:///{db_path}")

    yield engine

    engine.dispose(close=True)

    import os
    import sys
    import time

    if sys.platform == "win32":
        time.sleep(0.1)

    max_retries = 5
    for attempt in range(max_retries):
        try:
            os.unlink(db_path)
            break
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(0.1)
            else:
                raise


@pytest.fixture
def test_user():
    """Create a test user."""
    return User(id=ZERO_UUID, name="Test User")


@pytest.fixture
def test_project():
    """Create a test project."""
    return Project(
        id=ZERO_UUID,
        name="Test Project",
        description="A test project",
    )


@pytest.fixture
def test_project_id():
    """Create a test project ID."""
    return new_id()


@pytest.fixture
def metadata_storage(sqlite_engine):
    """Create SQL metadata storage instance."""
    return SQLProjectMetadataStorage(sqlite_engine)
