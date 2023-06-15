import json
import os
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import UUID4
from pydantic import BaseModel
from pydantic import Field

from evidently.experimental.report_set import load_report_set
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite


class ProjectItem:
    def __init__(self, report: Union[Report, TestSuite]):
        self.report = report
        _, self.dashboard_info, self.additional_graphs = report._build_dashboard_info()


class Project(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    _dashboard: Optional[dict] = None  # should be DashboardInfo type
    path: str

    _reports: Optional[Dict[uuid.UUID, Report]] = None
    _test_suites: Optional[Dict[uuid.UUID, TestSuite]] = None
    _items: Optional[Dict[uuid.UUID, ProjectItem]] = None

    @property
    def reports(self) -> Dict[uuid.UUID, ProjectItem]:
        if self._items is None:
            self._items = {r.id: ProjectItem(r) for r in
                           list(load_report_set(os.path.join(self.path, "reports"), cls=Report).values())
                           + list(load_report_set(os.path.join(self.path, "test_suites"), cls=TestSuite).values())
                           }
        return {key: value for key, value in self._items.items() if isinstance(value.report, Report)}

    @property
    def test_suites(self) -> Dict[uuid.UUID, ProjectItem]:
        if self._items is None:
            self._items = {r.id: ProjectItem(r) for r in
                           list(load_report_set(os.path.join(self.path, "reports"), cls=Report).values())
                           + list(load_report_set(os.path.join(self.path, "test_suites"), cls=TestSuite).values())
                           }
        return {key: value for key, value in self._items.items() if isinstance(value.report, TestSuite)}

    def get_item(self, report_id: uuid.UUID) -> Optional[ProjectItem]:
        return self.reports.get(report_id) or self.test_suites.get(report_id)

    @property
    def dashboard(self) -> dict:
        if self._dashboard is None:
            with open(os.path.join(self.path, "dashboard.json"), "r") as f:
                self._dashboard = json.load(f)
        return self._dashboard

class Workspace:
    def __init__(self, path: str):
        self.path = path
        self._projects: Dict[uuid.UUID, Project] = self._load_projects()

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        # todo save/load projects metadata
        projects = [
            Project(name=p, path=os.path.join(self.path, p))
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def get_project(self, project_id: uuid.UUID) -> Project:
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())
