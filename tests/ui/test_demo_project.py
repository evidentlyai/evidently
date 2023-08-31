from evidently.ui.demo_project import DEMO_PROJECT_NAME
from evidently.ui.demo_project import create_demo_project
from evidently.ui.workspace import Workspace


def test_create_demo_proejct(tmp_path):
    create_demo_project(str(tmp_path))

    ws = Workspace(path=str(tmp_path))
    assert len(ws.search_project(DEMO_PROJECT_NAME)) > 0
