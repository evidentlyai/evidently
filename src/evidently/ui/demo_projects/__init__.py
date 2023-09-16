from typing import Dict

from .base import DemoProject
from .bikes import bikes_demo_project
from .other_bikes import other_bikes_demo_project
from .reviews import reviews_demo_project

DEMO_PROJECTS: Dict[str, DemoProject] = {
    "other_bikes": other_bikes_demo_project,
    "bikes": bikes_demo_project,
    "reviews": reviews_demo_project,
}
