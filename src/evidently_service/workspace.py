import datetime
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
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.utils import NumpyEncoder
from evidently_service.dashboards import DashboardConfig
from evidently_service.dashboards import DashboardPanel

METADATA_PATH = "metadata.json"
REPORTS_PATH = "reports"
TEST_SUITES_PATH = "test_suites"


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
    dashboard: DashboardConfig

    _reports: Optional[Dict[uuid.UUID, Report]] = None
    _test_suites: Optional[Dict[uuid.UUID, TestSuite]] = None
    _items: Optional[Dict[uuid.UUID, ProjectItem]] = None
    _workspace: "Workspace"

    @property
    def items(self):
        if not hasattr(self, "_items") or self._items is None:
            self._items = {}
        return self._items

    @property
    def path(self):
        return os.path.join(self.workspace.path, str(self.id))

    @property
    def workspace(self) -> "Workspace":
        if not hasattr(self, "_workspace"):
            raise ValueError("Project is not binded to workspace")
        return self._workspace

    def bind(self, workspace: "Workspace"):
        self._workspace = workspace
        return self

    def add_panel(self, panel: DashboardPanel):
        self.dashboard.panels.append(panel)

    def add_item(self, item: Union[Report, TestSuite]):
        item_dir = REPORTS_PATH if isinstance(item, Report) else TEST_SUITES_PATH
        item._save(os.path.join(self.path, item_dir, str(item.id) + ".json"))
        self.items[item.id] = ProjectItem(item)

    def add_report(self, report: Report):
        self.add_item(report)

    def add_test_suite(self, test_suite: TestSuite):
        self.add_item(test_suite)

    @classmethod
    def load(cls, path: str) -> "Project":
        try:
            with open(os.path.join(path, METADATA_PATH)) as f:
                return parse_obj_as(Project, json.load(f))
        except FileNotFoundError:
            return Project(name="Unnamed Project", dashboard=DashboardConfig(name="Dashboard", panels=[]))

    def save(self):
        os.makedirs(os.path.join(self.path, REPORTS_PATH), exist_ok=True)
        os.makedirs(os.path.join(self.path, TEST_SUITES_PATH), exist_ok=True)
        with open(os.path.join(self.path, METADATA_PATH), "w") as f:
            return json.dump(self.dict(), f, indent=2, cls=NumpyEncoder)

    def reload(self):
        project = self.load(self.path).bind(self.workspace)
        self.__dict__.update(project.__dict__)

    def _load_items(self):
        self._items = {
            r.id: ProjectItem(r)
            for r in list(load_report_set(os.path.join(self.path, "reports"), cls=Report).values())
            + list(load_report_set(os.path.join(self.path, "test_suites"), cls=TestSuite).values())
        }

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        # if self._items is None:
        self._load_items()
        return {key: value.report for key, value in self._items.items() if isinstance(value.report, Report)}

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        # if self._items is None:
        self._load_items()
        return {key: value.report for key, value in self._items.items() if isinstance(value.report, TestSuite)}

    def get_item(self, report_id: uuid.UUID) -> Optional[ProjectItem]:
        item = self.reports.get(report_id) or self.test_suites.get(report_id)
        if item is None:
            return None
        return self._items.get(item.id)

    def build_dashboard_info(
        self, timestamp_start: Optional[datetime.datetime], timestamp_end: Optional[datetime.datetime]
    ) -> DashboardInfo:
        self.reload()
        return self.dashboard.build_dashboard_info(
            [
                r
                for r in self.reports.values()
                if (timestamp_start is None or r.timestamp >= timestamp_start)
                and (timestamp_end is None or r.timestamp < timestamp_end)
            ]
        )


class Workspace:
    def __init__(self, path: str):
        self.path = path
        self._projects: Dict[uuid.UUID, Project] = self._load_projects()

    @classmethod
    def create(cls, path: str):
        os.makedirs(path, exist_ok=True)
        return Workspace(path=path)

    def add_project(self, name: str, description: Optional[str] = None) -> Project:
        project = Project(name=name, description=description, dashboard=DashboardConfig(name=name, panels=[])).bind(
            self
        )
        project.save()
        return project

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        projects = [
            Project.load(os.path.join(self.path, p)).bind(self)
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def get_project(self, project_id: uuid.UUID) -> Project:
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())
