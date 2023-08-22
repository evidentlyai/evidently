import abc
import datetime
import json
import os
import shutil
import uuid
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from pydantic import UUID4
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from pydantic import parse_obj_as

from evidently.model.dashboard import DashboardInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.notebook_utils import determine_template
from evidently.report import Report
from evidently.suite.base_suite import ReportBase
from evidently.suite.base_suite import Snapshot
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import DashboardConfig
from evidently.utils import NumpyEncoder
from evidently.utils.dashboard import TemplateParams

METADATA_PATH = "metadata.json"
SNAPSHOTS = "snapshots"


class ProjectSnapshot:
    project: "Project"
    id: uuid.UUID
    # todo: metadata

    # caches
    _value: Optional[Snapshot] = None
    _report: Optional[ReportBase] = None
    _dashboard_info: Optional[DashboardInfo] = None
    _additional_graphs: Optional[Dict[str, DetailsInfo]] = None

    def __init__(self, id: uuid.UUID, project: "Project", value: Optional[Snapshot] = None):
        self.id = id
        self.project = project
        self.last_modified_data = None
        if value is not None:
            self._value = value

    @property
    def value(self) -> Snapshot:
        if self._value is None:
            self.load()
        return self._value  # type: ignore[return-value]

    @property
    def report(self) -> ReportBase:
        if self._report is None:
            self._report = self.value.as_report() if self.value.is_report else self.value.as_test_suite()
        return self._report

    @property
    def dashboard_info(self):
        if self._dashboard_info is None:
            self.load()
        return self._dashboard_info

    @property
    def additional_graphs(self):
        if self._additional_graphs is None:
            self.load()
        return self._additional_graphs

    @property
    def path(self):
        return os.path.join(self.project.path, SNAPSHOTS, str(self.id) + ".json")

    def load(self):
        self._value = Snapshot.load(self.path)
        _, self._dashboard_info, self._additional_graphs = self.report._build_dashboard_info()


WST = TypeVar("WST", bound="WorkspaceBase")


class ProjectBase(BaseModel, Generic[WST]):
    class Config:
        underscore_attrs_are_private = True

    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    dashboard: DashboardConfig
    date_from: Optional[datetime.datetime] = None
    date_to: Optional[datetime.datetime] = None

    _workspace: "WST"

    @property
    def workspace(self) -> "WST":
        if not hasattr(self, "_workspace"):
            raise ValueError("Project is not binded to workspace")
        return self._workspace

    def bind(self, workspace: "WST"):
        self._workspace = workspace
        return self

    def save(self):
        raise NotImplementedError


class Project(ProjectBase["Workspace"]):
    _snapshots: Dict[uuid.UUID, ProjectSnapshot] = {}

    @property
    def path(self):
        return os.path.join(self.workspace.path, str(self.id))

    def add_snapshot(self, snapshot: Snapshot):
        item = ProjectSnapshot(snapshot.id, self, snapshot)
        snapshot.save(item.path)
        self._snapshots[item.id] = item

    def delete_snapshot(self, snapshot_id: Union[str, uuid.UUID]):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid.UUID(snapshot_id)
        if snapshot_id in self._snapshots:
            del self._snapshots[snapshot_id]
        path = os.path.join(self.path, SNAPSHOTS, f"{snapshot_id}.json")
        if os.path.exists(path):
            os.unlink(path)

    @classmethod
    def load(cls, path: str) -> "Project":
        try:
            with open(os.path.join(path, METADATA_PATH)) as f:
                return parse_obj_as(Project, json.load(f))
        except FileNotFoundError:
            return Project(name="Unnamed Project", dashboard=DashboardConfig(name="Dashboard", panels=[]))

    def save(self):
        os.makedirs(os.path.join(self.path, SNAPSHOTS), exist_ok=True)
        with open(os.path.join(self.path, METADATA_PATH), "w") as f:
            return json.dump(self.dict(), f, indent=2, cls=NumpyEncoder)

    def reload(self):
        project = self.load(self.path).bind(self.workspace)
        self.__dict__.update(project.__dict__)

    def _reload_snapshots(self, skip_errors=True):
        path = os.path.join(self.path, SNAPSHOTS)
        for file in os.listdir(path):
            snapshot_id = uuid.UUID(file[: -len(".json")])
            if snapshot_id in self._snapshots:
                continue
            self.reload_snapshot(snapshot_id, skip_errors)

    def reload_snapshot(self, snapshot_id: Union[str, uuid.UUID], skip_errors=True):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid.UUID(snapshot_id)
        path = os.path.join(self.path, SNAPSHOTS, str(snapshot_id) + ".json")
        try:
            suite = Snapshot.load(path)
            self._snapshots[snapshot_id] = ProjectSnapshot(snapshot_id, self, suite)
        except ValidationError:
            if not skip_errors:
                raise

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        self._reload_snapshots()
        return {key: value.value.as_report() for key, value in self._snapshots.items() if value.value.is_report}

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        self._reload_snapshots()
        return {key: value.value.as_test_suite() for key, value in self._snapshots.items() if not value.value.is_report}

    def get_snapshot(self, id: uuid.UUID) -> Optional[ProjectSnapshot]:
        self._reload_snapshots()
        return self._snapshots.get(id, None)

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

    def show_dashboard(
        self, timestamp_start: Optional[datetime.datetime] = None, timestamp_end: Optional[datetime.datetime] = None
    ):
        dashboard_info = self.build_dashboard_info(timestamp_start, timestamp_end)
        template_params = TemplateParams(
            dashboard_id="pd_" + str(uuid.uuid4()).replace("-", ""),
            dashboard_info=dashboard_info,
            additional_graphs={},
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(determine_template("inline")(params=template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err


PT = TypeVar("PT", bound=ProjectBase)

STR_UUID = Union[str, uuid.UUID]


class WorkspaceBase(abc.ABC, Generic[PT]):
    @abc.abstractmethod
    def create_project(self, name: str, description: Optional[str] = None) -> PT:
        raise NotImplementedError

    @abc.abstractmethod
    def add_project(self, project: ProjectBase) -> PT:
        raise NotImplementedError

    @abc.abstractmethod
    def get_project(self, project_id: uuid.UUID) -> Optional[PT]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_project(self, project_id: STR_UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def list_projects(self) -> List[PT]:
        raise NotImplementedError

    def add_report(self, project_id: STR_UUID, report: Report):
        self.add_snapshot(project_id, report.to_snapshot())

    def add_test_suite(self, project_id: STR_UUID, test_suite: TestSuite):
        self.add_snapshot(project_id, test_suite.to_snapshot())

    @abc.abstractmethod
    def add_snapshot(self, project_id: STR_UUID, snapshot: Snapshot):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def search_project(self, project_name: str) -> List[PT]:
        raise NotImplementedError


class Workspace(WorkspaceBase[Project]):
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

    def add_project(self, project: ProjectBase) -> Project:
        if not isinstance(project, Project):
            project = Project(**project.dict())
        project.bind(self)
        project_id = str(project.id)
        os.makedirs(os.path.join(self.path, project_id, SNAPSHOTS), exist_ok=True)
        with open(os.path.join(self.path, project_id, METADATA_PATH), "w") as f:
            json.dump(project.dict(), f, indent=2, cls=NumpyEncoder)
        self._projects[project.id] = project
        return project

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        projects = [
            Project.load(os.path.join(self.path, p)).bind(self)
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())

    def add_snapshot(self, project_id: STR_UUID, snapshot: Snapshot):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].add_snapshot(snapshot)

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].delete_snapshot(snapshot_id)

    def search_project(self, project_name: str) -> List[Project]:
        return [p for p in self._projects.values() if p.name == project_name]

    def reload_project(self, project_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        project = Project.load(os.path.join(self.path, str(project_id))).bind(self)
        self._projects[project.id] = project

    def delete_project(self, project_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        if project_id in self._projects:
            del self._projects[project_id]
        path = os.path.join(self.path, str(project_id))
        if os.path.exists(path):
            shutil.rmtree(path)


def upload_snapshot(item: ReportBase, workspace_or_url: Union[str, WorkspaceBase], project_id: Union[uuid.UUID, str]):
    if isinstance(workspace_or_url, WorkspaceBase):
        workspace_or_url.add_snapshot(project_id, item.to_snapshot())
        return

    if os.path.exists(workspace_or_url):
        workspace: WorkspaceBase = Workspace(path=workspace_or_url)
    else:
        from evidently.ui.remote import RemoteWorkspace

        workspace = RemoteWorkspace(workspace_or_url)

    workspace.add_snapshot(project_id, item.to_snapshot())
