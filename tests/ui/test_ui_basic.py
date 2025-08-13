import pytest
from litestar.testing import TestClient

from evidently.ui.service.app import create_app
from evidently.ui.service.demo_projects import DEMO_PROJECTS
from evidently.ui.service.local_service import LocalConfig
from tests.conftest import slow


@pytest.fixture
def test_client(tmp_path):
    dp = DEMO_PROJECTS["bikes"]
    dp.create(str(tmp_path))
    config = LocalConfig()
    config.storage.path = str(tmp_path)

    return TestClient(create_app(config=config))


@slow
def test_root_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
