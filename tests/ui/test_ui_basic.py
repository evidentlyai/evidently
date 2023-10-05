import pytest
from fastapi.testclient import TestClient

from evidently.ui.app import app
from evidently.ui.demo_projects import DEMO_PROJECTS
from evidently.ui.workspace import Workspace

client = TestClient(app)


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


@pytest.mark.usefixtures("demo_project_workspace")
def test_api_project():
    response = client.get("/api/projects")
    assert response.status_code == 200
