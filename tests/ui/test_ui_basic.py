import pytest
from fastapi.testclient import TestClient

from evidently.ui.app import app
from evidently.ui.config import Configuration
from evidently.ui.demo_projects import DEMO_PROJECTS
from evidently.ui.workspace import Workspace

client = TestClient(app)
app.state.config = Configuration()  # todo: make it a fixture


@pytest.fixture
def demo_project_workspace(tmp_path):
    dp = DEMO_PROJECTS["bikes"]
    dp.create(str(tmp_path))
    ws = Workspace(path=str(tmp_path))
    app.state.workspace = ws
    yield
    app.state.workspace = None


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200


def test_remote_verify_route():
    response = client.get("/api/version")
    assert response.status_code == 200
    version_response = response.json()
    assert "version" in version_response
    assert version_response["application"] == "Evidently UI"


@pytest.mark.usefixtures("demo_project_workspace")
def test_api_project():
    response = client.get("/api/projects")
    assert response.status_code == 200
