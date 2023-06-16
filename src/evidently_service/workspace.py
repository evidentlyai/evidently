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
from pydantic import parse_obj_as

from evidently.experimental.report_set import load_report_set
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently_service.dashboards import DashboardConfig

DASHBOARDS_PATH = "dashboards.json"


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
    path: str

    _reports: Optional[Dict[uuid.UUID, Report]] = None
    _dashboards: Optional[Dict[uuid.UUID, DashboardConfig]] = None
    _test_suites: Optional[Dict[uuid.UUID, TestSuite]] = None
    _items: Optional[Dict[uuid.UUID, ProjectItem]] = None

    def _load_items(self):
        self._items = {
            r.id: ProjectItem(r)
            for r in list(load_report_set(os.path.join(self.path, "reports"), cls=Report).values())
            + list(load_report_set(os.path.join(self.path, "test_suites"), cls=TestSuite).values())
        }

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        if self._items is None:
            self._load_items()
        return {key: value.report for key, value in self._items.items() if isinstance(value.report, Report)}

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        if self._items is None:
            self._load_items()
        return {key: value.report for key, value in self._items.items() if isinstance(value.report, TestSuite)}

    def get_item(self, report_id: uuid.UUID) -> Optional[ProjectItem]:
        return self.reports.get(report_id) or self.test_suites.get(report_id)

    @property
    def dashboards(self) -> Dict[uuid.UUID, DashboardConfig]:
        if self._dashboards is None:
            try:
                with open(os.path.join(self.path, DASHBOARDS_PATH)) as f:
                    self._dashboards = parse_obj_as(Dict[uuid.UUID, DashboardConfig], json.load(f))
            except FileNotFoundError:
                return {}
        return self._dashboards


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
