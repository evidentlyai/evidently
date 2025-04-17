import os
from typing import Optional

import uuid6
from typer import BadParameter
from typer import Option
from typer import echo

from evidently.cli.main import app
from evidently.legacy.ui.demo_projects import DEMO_PROJECTS_NAMES


def setup_deterministic_generation_uuid(seed: int = 8754):
    import uuid

    from faker import Faker

    Faker.seed(seed)
    fake = Faker()

    def deterministic_uuid():
        return fake.uuid4(cast_to=None)

    uuid.uuid4 = deterministic_uuid
    uuid6.uuid7 = deterministic_uuid


@app.command("legacy_ui")
def legacy_ui(
    host: str = Option("127.0.0.1", help="Service host"),
    port: int = Option(8000, help="Service port"),
    workspace: str = Option("workspace", help="Path to workspace"),
    demo_projects: str = Option(
        "",
        "--demo-projects",
        help=f"Comma-separated list of demo projects to generate. Possible values: [{'|'.join(['all'] + DEMO_PROJECTS_NAMES)}]",
    ),
    secret: Optional[str] = Option(None, help="Secret for writing operations"),
):
    """Start Evidently UI service (legacy version)"""
    if os.environ.get("EXPERIMENTAL_DETERMINISTIC_UUID"):
        setup_deterministic_generation_uuid()

    from evidently.legacy.ui.app import run_local
    from evidently.legacy.ui.demo_projects import DEMO_PROJECTS
    from evidently.legacy.ui.workspace import Workspace

    demos = demo_projects.split(",") if demo_projects else []
    if "all" in demos:
        demos = DEMO_PROJECTS_NAMES
    missing = [dp for dp in demos if dp not in DEMO_PROJECTS]
    if missing:
        raise BadParameter(f"Unknown demo project name '{missing[0]}'")

    if demos:
        ws = Workspace.create(workspace)
        for demo_project in demos:
            dp = DEMO_PROJECTS[demo_project]

            has_demo_project = any(p.name == dp.name for p in ws.list_projects())
            if not has_demo_project:
                echo(f"Generating demo project '{dp.name}'...")
                dp.create(workspace)
    run_local(host, port, workspace, secret)
