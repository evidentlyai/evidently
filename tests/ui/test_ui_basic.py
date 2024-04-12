import pytest
from litestar.testing import TestClient

from evidently.ui.app import create_app
from evidently.ui.demo_projects import DEMO_PROJECTS
from evidently.ui.local_service import LocalConfig
from tests.conftest import slow


@pytest.fixture
def test_client():
    return TestClient(create_app(config=LocalConfig()))


@pytest.fixture
def test_client_with_demo(tmp_path):
    dp = DEMO_PROJECTS["bikes"]
    dp.create(str(tmp_path))
    config = LocalConfig()
    config.storage.path = str(tmp_path)

    return TestClient(create_app(config=config))


@slow
def test_root_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


@slow
def test_remote_verify_route(test_client):
    response = test_client.get("/api/version")
    assert response.status_code == 200
    version_response = response.json()
    assert "version" in version_response
    assert version_response["application"] == "Evidently UI"


@slow
def test_api_project(test_client_with_demo):
    response = test_client_with_demo.get("/api/projects")
    assert response.status_code == 200
