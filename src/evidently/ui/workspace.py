import abc
import datetime
import json
import os
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from pydantic import UUID4
from pydantic import BaseModel
from pydantic import Field
from pydantic import parse_obj_as

from evidently.experimental.report_set import load_report_set
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import DashboardConfig
from evidently.ui.dashboards import DashboardPanel
from evidently.utils import NumpyEncoder

METADATA_PATH = "metadata.json"
REPORTS_PATH = "reports"
TEST_SUITES_PATH = "test_suites"


class ProjectItem:
    def __init__(self, report: Union[Report, TestSuite]):
        self.report = report
        self.last_modified_date = None
        self._dashboard_info = None
        self._additional_graphs = None

    @property
    def dashboard_info(self):
        if self._dashboard_info is None:
            self._load()
        return self._dashboard_info

    @property
    def additional_graphs(self):
        if self._additional_graphs is None:
            self._load()
        return self._additional_graphs

    def _load(self):
        _, self._dashboard_info, self._additional_graphs = self.report._build_dashboard_info()


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
    _cached_graphs: Optional[Dict[Tuple[uuid.UUID, str], dict]] = None
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
        return {key: value.report for key, value in self.items.items() if isinstance(value.report, Report)}

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        # if self._items is None:
        self._load_items()
        return {key: value.report for key, value in self.items.items() if isinstance(value.report, TestSuite)}

    def get_item(self, report_id: uuid.UUID) -> Optional[ProjectItem]:
        item = self.reports.get(report_id) or self.test_suites.get(report_id)
        if item is None:
            return None
        project_item = self.items.get(item.id)
        if project_item is None:
            return None
        for graph_id, graph_data in project_item.additional_graphs.items():
            self.cached_graphs[(report_id, graph_id)] = graph_data
        return self.items.get(item.id)

    @property
    def cached_graphs(self):
        if self._cached_graphs is None:
            self._cached_graphs = {}
        return self._cached_graphs

    def get_additional_graph_info(self, report_id: uuid.UUID, graph_id: str) -> Optional[dict]:
        return self.cached_graphs.get((report_id, graph_id))

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


class WorkspaceBase(abc.ABC):
    @abc.abstractmethod
    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def add_project(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get_project(self, project_id: uuid.UUID) -> Optional[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_projects(self) -> List[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_report(self, project_id: Union[str, uuid.UUID], report: Report):
        raise NotImplementedError

    @abc.abstractmethod
    def add_test_suite(self, project_id: Union[str, uuid.UUID], test_suite: TestSuite):
        raise NotImplementedError


class Workspace(WorkspaceBase):
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)
        self._projects: Dict[uuid.UUID, Project] = self._load_projects()

    @classmethod
    def create(cls, path: str):
        os.makedirs(path, exist_ok=True)
        return Workspace(path=path)

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        project = Project(name=name, description=description, dashboard=DashboardConfig(name=name, panels=[]))
        return self.add_project(project)

    def add_project(self, project: Project) -> Project:
        project.bind(self)
        project.save()
        self._projects[project.id] = project
        return project

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        projects = [
            Project.load(os.path.join(self.path, p)).bind(self)
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def get_project(self, project_id: Union[str, uuid.UUID]) -> Optional[Project]:
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())

    def add_report(self, project_id: Union[str, uuid.UUID], report: Report):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].add_report(report)

    def add_test_suite(self, project_id: Union[str, uuid.UUID], test_suite: TestSuite):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].add_test_suite(test_suite)


def upload_item(
    item: Union[Report, TestSuite], workspace_or_url: Union[str, Workspace], project_id: Union[uuid.UUID, str]
):
    if isinstance(workspace_or_url, Workspace):
        project = workspace_or_url.get_project(project_id)
        if project is None:
            raise ValueError(f"Project {project_id} not found")
        project.add_item(item)
        return

    if os.path.exists(workspace_or_url):
        workspace = Workspace(path=workspace_or_url)
        project = workspace.get_project(project_id)
        if project is None:
            raise ValueError(f"Project {project_id} not found")
        project.add_item(item)
        return

    from evidently.ui.remote import RemoteWorkspace

    client = RemoteWorkspace(workspace_or_url)
    if isinstance(item, Report):
        client.add_report(project_id, item)
    else:
        client.add_test_suite(project_id, item)
