from evidently.cli.main import app
from evidently.cli.ui import ui
from evidently.legacy.cli.ui import ui as legacy_ui

__all__ = ["app", "ui", "legacy_ui"]

if __name__ == "__main__":
    app()
