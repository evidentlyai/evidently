import pytest

from evidently.ui.demo_projects import DEMO_PROJECTS
from evidently.ui.workspace import Workspace


@pytest.mark.parametrize("demo_project", list(DEMO_PROJECTS.keys()))
def test_create_demo_project(demo_project, tmp_path):
    dp = DEMO_PROJECTS[demo_project]
    dp.create(str(tmp_path))

    ws = Workspace(path=str(tmp_path))
    assert len(ws.search_project(dp.name)) > 0
