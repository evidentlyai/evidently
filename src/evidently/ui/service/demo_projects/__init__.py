from typing import Dict

from .base import DemoProject
from .bikes import bikes_demo_project

DEMO_PROJECTS: Dict[str, DemoProject] = {
    "bikes": bikes_demo_project,
}

DEMO_PROJECTS_NAMES = list(DEMO_PROJECTS.keys())

__all__ = [
    "DemoProject",
    "DEMO_PROJECTS",
    "bikes_demo_project",
]
