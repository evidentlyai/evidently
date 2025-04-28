import sys

from typer import Option
from typer import echo

from evidently.cli.main import app
from evidently.ui.service.demo_projects import DEMO_PROJECTS


@app.command("demo_project")
def generate_demo_project(
    project: str = Option("all", help="Project to generate"),
    path: str = Option("workspace", help="Workspace path"),
):
    _project = DEMO_PROJECTS.get(project)
    if _project is None:
        echo(f"Demo project {project} not found.")
        sys.exit(1)
    _project.create(path)
