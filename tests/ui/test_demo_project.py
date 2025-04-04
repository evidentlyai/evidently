import pytest

from evidently.legacy.ui.demo_projects import DEMO_PROJECTS
from evidently.legacy.ui.demo_projects import DEMO_PROJECTS_NAMES
from evidently.legacy.ui.workspace import Workspace
from tests.conftest import slow


@slow
@pytest.mark.parametrize("demo_project", DEMO_PROJECTS_NAMES)
def test_create_demo_project(demo_project, tmp_path):
    dp = DEMO_PROJECTS[demo_project]
    dp.count = 2
    dp.create(str(tmp_path))

    ws = Workspace(path=str(tmp_path))
    assert len(ws.search_project(dp.name)) > 0
