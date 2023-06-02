import os
from typing import List

from evidently.experimental.report_set import load_report_set
from evidently.report import Report


class Workspace:
    def __init__(self, path: str):
        self.path = path

    def list_projects(self) -> List[str]:
        return [p for p in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, p))]

    def list_project_reports(self, project_name: str) -> List[Report]:
        return list(load_report_set(os.path.join(self.path, project_name), cls=Report).values())
