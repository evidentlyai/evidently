import os
import sys
from typing import Optional
from typing import cast

from typer import Option
from typer import echo

from evidently.cli.main import app
from evidently.cli.ui import setup_deterministic_generation_uuid
from evidently.ui.service.demo_projects import DEMO_PROJECTS
from evidently.ui.service.demo_projects import DemoProjectsNames
from evidently.ui.workspace import RemoteWorkspace
from evidently.ui.workspace import WorkspaceBase


@app.command("demo_project")
def generate_demo_project(
    project: str = Option("all", help="Project to generate"),
    path: str = Option("workspace", help="Workspace path or URL (if starts with http)"),
    secret: Optional[str] = Option(None, help="Secret for remote workspace authentication"),
):
    if os.environ.get("EXPERIMENTAL_DETERMINISTIC_UUID"):
        setup_deterministic_generation_uuid()
    # TODO: better type safety
    _project = DEMO_PROJECTS.get(cast(DemoProjectsNames, project))
    if _project is None:
        echo(f"Demo project {project} not found.")
        sys.exit(1)

    # If path starts with http, use RemoteWorkspace; otherwise use local Workspace
    if path.startswith("http"):
        secret = secret or os.environ.get("EVIDENTLY_SECRET")
        ws: WorkspaceBase = RemoteWorkspace(path, secret=secret)
        _project.create(ws)
    else:
        _project.create(path)
