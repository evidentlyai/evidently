from typing import Optional

import typer
from typer import Option

from evidently.cli.main import app


@app.command("ui")
def ui(
    host: str = Option("0.0.0.0", help="Service host"),
    port: int = Option(8000, help="Service port"),
    workspace: str = Option("workspace", help="Path to workspace"),
    demo_project: bool = Option(False, "--demo-project", is_flag=True, help="Generate demo project"),
    secret: Optional[str] = Option(None, help="Secret for writing operations"),
):
    """Start Evidently UI service"""
    from evidently.ui.app import run
    from evidently.ui.demo_project import DEMO_PROJECT_NAME
    from evidently.ui.demo_project import create_demo_project
    from evidently.ui.workspace import Workspace

    if demo_project:
        ws = Workspace.create(workspace)
        has_demo_project = any(p.name == DEMO_PROJECT_NAME for p in ws.list_projects())
        if not has_demo_project:
            typer.echo("Generating demo project...")
            create_demo_project(workspace)
    run(host, port, workspace, secret)
