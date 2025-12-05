import os
import threading
import time
from typing import Optional
from typing import cast

import requests
import uuid6
from typer import BadParameter
from typer import Option
from typer import echo

from evidently.cli.main import app
from evidently.ui.service.app import get_config
from evidently.ui.service.demo_projects import DEMO_PROJECT_NAMES_FOR_CLI
from evidently.ui.service.demo_projects import DEMO_PROJECTS
from evidently.ui.service.demo_projects import DEMO_PROJECTS_NAMES
from evidently.ui.service.demo_projects import DemoProjectsNames
from evidently.ui.workspace import RemoteWorkspace


def setup_deterministic_generation_uuid(seed: int = 8754):
    import uuid

    from faker import Faker

    Faker.seed(seed)
    fake = Faker()

    def deterministic_uuid():
        return fake.uuid4(cast_to=None)

    uuid.uuid4 = deterministic_uuid
    uuid6.uuid7 = deterministic_uuid


def _create_demo_projects_task(demo_names: list[str], host: str, port: int, secret: Optional[str]):
    """Background task that waits for server and creates demo projects."""
    base_url = f"http://{host}:{port}"

    # Wait for server to be ready by polling /api/version
    max_retries = 30
    retry_delay = 0.5
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{base_url}/api/version", timeout=1)
            if response.status_code == 200:
                break
        except Exception:
            pass

        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            echo(f"Warning: Could not connect to server at {base_url} after {max_retries} attempts")
            return

    # Create demo projects using RemoteWorkspace
    try:
        ws = RemoteWorkspace(base_url, secret=secret)

        for demo_name in demo_names:
            if demo_name not in DEMO_PROJECTS:
                echo(f"Warning: Unknown demo project: {demo_name}")
                continue

            # TODO: better type safety
            demo_project = DEMO_PROJECTS[cast(DemoProjectsNames, demo_name)]

            # Check if project already exists
            existing_projects = ws.list_projects()
            has_demo_project = any(p.name == demo_project.name for p in existing_projects)

            if not has_demo_project:
                echo(f"Creating demo project '{demo_project.name}'...")
                demo_project.create(ws)
                echo(f"Demo project '{demo_project.name}' created successfully")
            else:
                echo(f"Demo project '{demo_project.name}' already exists, skipping")

    except Exception as e:
        echo(f"Error creating demo projects: {e}")


@app.command("ui")
def ui(
    host: str = Option("127.0.0.1", help="Service host"),
    port: int = Option(8000, help="Service port"),
    workspace: str = Option("workspace", help="Path to workspace"),
    demo_projects: str = Option(
        "",
        "--demo-projects",
        help=f"Comma-separated list of demo projects to generate. Possible values: [{'|'.join(DEMO_PROJECT_NAMES_FOR_CLI)}]",
    ),
    secret: Optional[str] = Option(None, help="Secret for writing operations"),
    litestar_request_max_body_size: Optional[int] = Option(None, help="Request body size limit"),
    conf_path: Optional[str] = Option(None, help="Path to configuration file"),
):
    """Start Evidently UI service"""
    if os.environ.get("EXPERIMENTAL_DETERMINISTIC_UUID"):
        setup_deterministic_generation_uuid()

    from evidently.ui.service.app import run

    demos: list[str] = demo_projects.split(",") if demo_projects else []
    if "all" in demos:
        # TODO: better type safety
        demos = cast(list[str], list(DEMO_PROJECTS_NAMES))
    missing = [dp for dp in demos if dp not in DEMO_PROJECTS]
    if missing:
        raise BadParameter(f"Unknown demo project name '{missing[0]}'")

    if demos:
        # Start background task in a daemon thread
        thread = threading.Thread(
            target=_create_demo_projects_task,
            args=(demos, host, port, secret),
            daemon=True,
        )
        thread.start()

    config = get_config(
        host=host,
        port=port,
        workspace=workspace,
        secret=secret,
        request_max_body_size=litestar_request_max_body_size,
        conf_path=conf_path,
    )
    run(config)
