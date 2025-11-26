import json
import tempfile

import pytest
from litestar.testing import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from evidently._pydantic_compat import BaseModel
from evidently.legacy.core import new_id
from evidently.legacy.utils import NumpyEncoder
from evidently.ui.service.app import create_app
from evidently.ui.service.base import Project
from evidently.ui.service.base import User
from evidently.ui.service.local_service import LocalConfig
from evidently.ui.service.storage.sql.metadata import SQLProjectMetadataStorage
from evidently.ui.service.storage.sql.utils import migrate_database
from evidently.ui.service.type_aliases import ZERO_UUID

HEADERS = {"Content-Type": "application/json"}


@pytest.fixture
def sqlite_engine():
    """Create a temporary SQLite database for testing."""
    import gc
    import os
    import sys
    import time

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    # Use NullPool to avoid connection pooling issues on Windows
    engine = create_engine(f"sqlite:///{db_path}", poolclass=NullPool)
    migrate_database(f"sqlite:///{db_path}")

    yield engine

    # Close all connections and dispose the engine
    engine.dispose(close=True)

    # Force garbage collection to ensure all references are cleared
    gc.collect()

    # On Windows, files can't be deleted if they're still open
    # Wait longer and retry more times
    if sys.platform == "win32":
        time.sleep(0.2)

    max_retries = 10
    for attempt in range(max_retries):
        try:
            os.unlink(db_path)
            break
        except PermissionError:
            if attempt < max_retries - 1:
                # Increase wait time with each retry
                time.sleep(0.1 * (attempt + 1))
                # Force another garbage collection
                gc.collect()
            else:
                # On Windows, sometimes we need to just skip the cleanup
                # The temp file will be cleaned up by the OS eventually
                if sys.platform == "win32":
                    import warnings

                    warnings.warn(
                        f"Could not delete SQLite database file {db_path} on Windows. It will be cleaned up by the OS."
                    )
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


@pytest.fixture
def test_client(tmp_path):
    """Create a test client."""
    config = LocalConfig()
    config.storage.path = str(tmp_path)
    app = create_app(config=config)
    return TestClient(app=app)


@pytest.fixture
def mock_project():
    """Create a mock project."""
    return Project(name="mock", team_id=None)


def _dumps(obj: BaseModel):
    """Dump object to JSON string."""
    return json.dumps(obj.dict(), allow_nan=True, cls=NumpyEncoder)
