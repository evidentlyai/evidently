from evidently.cli.legacy_ui import legacy_ui
from evidently.cli.main import app
from evidently.cli.ui import ui

__all__ = ["app", "ui", "legacy_ui"]

if __name__ == "__main__":
    app()
