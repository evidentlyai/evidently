import sys
from pathlib import Path

from evidently.cli.demo_project import generate_demo_project
from evidently.cli.legacy_ui import legacy_ui
from evidently.cli.main import app
from evidently.cli.migrate import migrate
from evidently.cli.migrate import migrate_status
from evidently.cli.report import run_report
from evidently.cli.run import run_command
from evidently.cli.run import validate_config
from evidently.cli.ui import ui

__all__ = [
    "app",
    "ui",
    "legacy_ui",
    "generate_demo_project",
    "run_report",
    "run_command",
    "validate_config",
    "migrate",
    "migrate_status",
]

sys.path.append(str(Path.cwd()))
if __name__ == "__main__":
    app()
