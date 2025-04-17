import inspect

import pytest

from evidently.cli import app
from evidently.ui.service.demo_projects import DEMO_PROJECTS_NAMES


@pytest.fixture()
def ui_command():
    command = [c for c in app.registered_commands if c.name == "ui"][0]
    argspec = inspect.getfullargspec(command.callback)
    return dict(zip(argspec.annotations.keys(), argspec.defaults))


@pytest.mark.parametrize("demo_project", DEMO_PROJECTS_NAMES)
def test_all_demo_projects_in_help(demo_project, ui_command):
    assert demo_project in ui_command["demo_projects"].help
