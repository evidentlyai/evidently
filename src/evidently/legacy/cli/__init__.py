from evidently.legacy.cli.collector import collector
from evidently.legacy.cli.main import app
from evidently.legacy.cli.ui import ui

__all__ = ["app", "ui", "collector"]


def main():
    app()


if __name__ == "__main__":
    main()
