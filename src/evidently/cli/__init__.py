import sys
from pathlib import Path

from evidently.cli.demo_project import generate_demo_project
from evidently.cli.legacy_ui import legacy_ui
from evidently.cli.main import app
from evidently.cli.report import run_report
from evidently.cli.ui import ui

__all__ = ["app", "ui", "legacy_ui", "generate_demo_project", "run_report"]

sys.path.append(str(Path.cwd()))
if __name__ == "__main__":
    app()
