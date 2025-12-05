from typing import Dict
from typing import Literal
from typing import Union

from .base import DemoProject
from .bikes import bikes_demo_project
from .reviews import reviews_demo_project

DemoProjectsNames = Union[Literal["bikes"], Literal["reviews"]]

DEMO_PROJECTS: Dict[DemoProjectsNames, DemoProject] = {
    "bikes": bikes_demo_project,
    "reviews": reviews_demo_project,
}

DEMO_PROJECTS_NAMES = list(DEMO_PROJECTS.keys())
DEMO_PROJECT_NAMES_FOR_CLI = ["all"] + list(DEMO_PROJECTS.keys())

DemoProjectNamesForCliType = Union[Literal["all"], DemoProjectsNames]


__all__ = [
    "DemoProject",
    "DEMO_PROJECTS",
    "bikes_demo_project",
    "reviews_demo_project",
]
