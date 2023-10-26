from typing import Dict

from .adult import adult_demo_project
from .base import DemoProject
from .bikes import bikes_demo_project
from .reviews import reviews_demo_project

DEMO_PROJECTS: Dict[str, DemoProject] = {
    "bikes": bikes_demo_project,
    "reviews": reviews_demo_project,
    "adult": adult_demo_project,
}
