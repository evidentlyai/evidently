import abc
import io
import os
import uuid
from abc import ABC
from abc import abstractmethod
from json import JSONDecodeError
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Type
from typing import Union
from typing import overload

import pandas as pd
import uuid6
from requests import HTTPError
from requests import Response

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.report import Snapshot
from evidently.errors import EvidentlyError
from evidently.legacy.core import new_id
from evidently.legacy.ui.api.models import OrgModel
from evidently.legacy.ui.api.service import EVIDENTLY_APPLICATION_NAME
from evidently.legacy.ui.base import Org
from evidently.legacy.ui.storage.common import SECRET_HEADER_NAME
from evidently.legacy.ui.type_aliases import STR_UUID
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PanelID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TabID
from evidently.legacy.ui.workspace.cloud import ACCESS_TOKEN_COOKIE
from evidently.legacy.ui.workspace.cloud import TOKEN_HEADER_NAME
from evidently.legacy.ui.workspace.cloud import NamedBytesIO
from evidently.legacy.ui.workspace.cloud import read_multipart_response
from evidently.legacy.ui.workspace.remote import RemoteBase
from evidently.legacy.ui.workspace.remote import T


class DashboardTabModel(BaseModel):
    id: TabID = Field(default_factory=uuid6.uuid7)
    title: Optional[str]
    panels: List[PanelID]


class PanelMetric(BaseModel):
    legend: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
    metric: str
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    view_params: Dict[str, Any] = Field(default_factory=dict)


class DashboardPanelPlot(BaseModel):
    id: PanelID = Field(default_factory=uuid6.uuid7)
    title: str
    subtitle: Optional[str]
    size: Optional[str]
    values: List[PanelMetric]
    plot_params: Dict[str, Any] = Field(default_factory=dict)


class DashboardModel(BaseModel):
    tabs: List[DashboardTabModel]
    panels: List[DashboardPanelPlot]


class ProjectDashboard:
    @property
    @abc.abstractmethod
    def project_id(self) -> ProjectID:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tab(self, tab: str):
        raise NotImplementedError

    @abstractmethod
    def delete_tab(self, tab: str):
        raise NotImplementedError

    @abstractmethod
    def add_panel(self, panel: DashboardPanelPlot, tab: Optional[str], create_if_not_exists: bool = True):
        raise NotImplementedError

    @abstractmethod
    def delete_panel(self, panel: str, tab: str):
        raise NotImplementedError

    @abstractmethod
    def clear_tab(self, tag: str):
        raise NotImplementedError

    @abstractmethod
    def clear_dashboard(self):
        raise NotImplementedError

    @abstractmethod
    def model(self) -> DashboardModel:
        raise NotImplementedError

    def __repr__(self):
        _model = self.model()
        return f"Dashboard for project {self.project_id}\n  " + "\n  ".join(
            f"Tab '{tab.title}' ({tab.id})\n    "
            + "\n    ".join(
                f"Panel '{p.title}' ({p.id})\n      "
                + "\n      ".join(
                    f"Series metric_type={s.metric}"
                    + f" (tags={s.tags},metadata={s.metadata})"
                    + f" labels={s.metric_labels}"
                    for s in p.values
                )
                for p in _model.panels
                if p.id in tab.panels
            )
            for tab in _model.tabs
        )


class _RemoteProjectDashboard(ProjectDashboard):
    _project_id: ProjectID
    _workspace: "WorkspaceBase"

    def __init__(self, project_id: ProjectID, workspace: "WorkspaceBase"):
        self._project_id = project_id
        self._workspace = workspace

    @property
    def project_id(self) -> ProjectID:
        return self._project_id

    def add_tab(self, tab: str):
        _dashboard_model = self.model()
        if any([t.title == tab for t in _dashboard_model.tabs]):
            raise EvidentlyError(f"Tab {tab} already exists in project {self._project_id} dashboard")
        _dashboard_model.tabs.append(DashboardTabModel(title=tab, panels=[]))
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def delete_tab(self, tab: str):
        _dashboard_model = self.model()
        new_tabs = [t for t in _dashboard_model.tabs if t.title != tab]
        _dashboard_model.tabs = new_tabs
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def add_panel(self, panel: DashboardPanelPlot, tab: Optional[str] = None, create_if_not_exists: bool = True):
        _dashboard_model = self.model()
        _dashboard_model.panels.append(panel)
        _tab_id = None
        if tab is not None:
            for dashboard_tab in _dashboard_model.tabs:
                if dashboard_tab.title == tab:
                    dashboard_tab.panels.append(panel.id)
                    _tab_id = dashboard_tab.id
            if _tab_id is None and create_if_not_exists:
                new_tab_id = uuid.uuid4()
                _dashboard_model.tabs.append(DashboardTabModel(id=new_tab_id, title=tab, panels=[]))
                _tab_id = new_tab_id
            elif _tab_id is None and not create_if_not_exists:
                raise EvidentlyError(
                    f"Tab {tab} is missing in project {self._project_id} and create_if_not_exists is False"
                )
        else:
            if len(_dashboard_model.tabs) == 0:
                new_tab_id = uuid.uuid4()
                _dashboard_model.tabs.append(DashboardTabModel(id=new_tab_id, title="General", panels=[]))
            _tab_id = _dashboard_model.tabs[0].id

        assert _tab_id is not None
        for dashboard_tab in _dashboard_model.tabs:
            if dashboard_tab.id == _tab_id:
                dashboard_tab.panels.append(panel.id)
                break
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def delete_panel(self, panel: str, tab: str):
        _dashboard_model = self.model()
        _tab = None
        for t in _dashboard_model.tabs:
            if t.title == tab:
                _tab = t

        if _tab is None:
            raise EvidentlyError(f"Tab {tab} does not exist in project {self._project_id} dashboard")

        new_panels = [p for p in _dashboard_model.panels if p.id in _tab.panels and p.title != panel]
        _tab.panels = [p.id for p in new_panels]
        _dashboard_model.panels = new_panels

        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def model(self):
        return self._workspace.get_dashboard(self.project_id)

    def clear_tab(self, tab: str):
        _dashboard_model = self.model()
        _tab = None
        for t in _dashboard_model.tabs:
            if t.title == tab:
                _tab = t

        if _tab is None:
            raise EvidentlyError(f"Tab {tab} does not exist in project {self._project_id} dashboard")

        new_panels = [p for p in _dashboard_model.panels if p not in _tab.panels]
        _dashboard_model.panels = new_panels
        _tab.panels = []

        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def clear_dashboard(self):
        _dashboard_model = self.model()
        _dashboard_model.panels = []
        _dashboard_model.tabs = []
        self._workspace.save_dashboard(self.project_id, _dashboard_model)


class ProjectModel(BaseModel):
    id: ProjectID = Field(default_factory=new_id)
    name: str
    description: Optional[str] = None
    org_id: Optional[OrgID] = None
    version: str = "2"


class Project:
    _project: ProjectModel
    _dashboard: ProjectDashboard
    _workspace: "WorkspaceBase"

    def __init__(
        self,
        project: ProjectModel,
        dashboard: ProjectDashboard,
        workspace: "WorkspaceBase",
    ):
        self._project = project
        self._workspace = workspace
        self._dashboard = dashboard

    @property
    def id(self) -> ProjectID:
        return self._project.id

    @property
    def name(self) -> str:
        return self._project.name

    @name.setter
    def name(self, value: str):
        self._project.name = value

    @property
    def description(self) -> Optional[str]:
        return self._project.description

    @description.setter
    def description(self, value: str):
        self._project.description = value

    def save(self):
        self._workspace.update_project(self._project)

    @property
    def dashboard(self) -> ProjectDashboard:
        return self._dashboard

    def __repr__(self):
        return f"""Project ID: {self.id}
Project Name: {self.name}
Project Description: {self.description}
        """

    def dict(self):
        return self._project.dict()

    @property
    def version(self):
        return self._project.version


class SnapshotLink(BaseModel):
    snapshot_id: SnapshotID
    dataset_type: str
    dataset_subtype: str


class WorkspaceBase(ABC):
    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        org_id: Optional[OrgID] = None,
    ) -> Project:
        project = self.add_project(
            ProjectModel(
                name=name,
                description=description,
                org_id=org_id,
            ),
            org_id,
        )
        return project

    @abstractmethod
    def add_project(self, project: ProjectModel, org_id: Optional[OrgID] = None) -> Project:
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: STR_UUID):
        raise NotImplementedError

    @abstractmethod
    def list_projects(self, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project: ProjectModel):
        raise NotImplementedError

    @abstractmethod
    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot) -> SnapshotID:
        raise NotImplementedError

    def add_run(self, project_id: STR_UUID, run: Snapshot, include_data: bool = False) -> SnapshotID:
        snapshot_id = self._add_run(project_id, run)
        if include_data:
            current, reference = run.context._input_data
            self.add_dataset(
                project_id,
                current,
                f"run-current-{snapshot_id}",
                None,
                link=SnapshotLink(snapshot_id=snapshot_id, dataset_type="output", dataset_subtype="current"),
            )
            if reference is not None:
                self.add_dataset(
                    project_id,
                    reference,
                    f"run-reference-{snapshot_id}",
                    None,
                    link=SnapshotLink(snapshot_id=snapshot_id, dataset_type="output", dataset_subtype="reference"),
                )
        return snapshot_id

    @abstractmethod
    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        raise NotImplementedError

    @abstractmethod
    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        raise NotImplementedError

    @abstractmethod
    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str],
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        raise NotImplementedError

    @abc.abstractmethod
    def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        raise NotImplementedError

    @abc.abstractmethod
    def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        raise NotImplementedError


class Workspace(WorkspaceBase, ABC):  # todo: local workspace after UI for v2
    pass


class RemoteWorkspace(RemoteBase, WorkspaceBase):  # todo: reuse cloud ws
    def get_url(self):
        return self.base_url

    def verify(self):
        try:
            response = self._request("/api/version", "GET")
            assert response.json()["application"] == EVIDENTLY_APPLICATION_NAME
        except (HTTPError, JSONDecodeError, KeyError, AssertionError) as e:
            raise ValueError(f"Evidently API not available at {self.base_url}") from e

    def __init__(self, base_url: str, secret: Optional[str] = None):
        self.base_url = base_url
        self.secret = secret
        self.verify()

    def _prepare_request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ):
        r = super()._prepare_request(
            path=path,
            method=method,
            query_params=query_params,
            body=body,
            cookies=cookies,
            headers=headers,
            form_data=form_data,
        )
        if self.secret is not None:
            r.headers[SECRET_HEADER_NAME] = self.secret
        return r

    def add_project(self, project: ProjectModel, org_id: Optional[OrgID] = None) -> Project:
        params = {}
        if org_id:
            params["org_id"] = str(org_id)
        project_id = self._request(
            "/api/v2/projects", "POST", query_params=params, body=project.dict(), response_model=ProjectID
        )
        p = self.get_project(project_id)
        if p is None:
            raise EvidentlyError(
                f"Failed to receive updated information about project" f" after creation (project_id={project_id})"
            )
        return p

    def get_project(self, project_id: STR_UUID) -> Optional["Project"]:
        try:
            _project = self._request(f"/api/projects/{project_id}/info", "GET", response_model=ProjectModel)
            return Project(
                project=_project,
                dashboard=_RemoteProjectDashboard(_project.id, self),
                workspace=self,
            )
        except (HTTPError,) as e:
            try:
                data = e.response.json()  # type: ignore[attr-defined]
                if "detail" in data and data["detail"] == "project not found":
                    return None
                raise e
            except (ValueError, AttributeError):
                raise e

    def delete_project(self, project_id: STR_UUID):
        return self._request(f"/api/v2/projects/{project_id}", "DELETE")

    def list_projects(self, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        projects = self._request("/api/v2/projects", "GET", response_model=List[ProjectModel])
        return [Project(p, _RemoteProjectDashboard(p.id, self), self) for p in projects]

    def update_project(self, project: ProjectModel):
        self._request(
            f"/api/v2/projects/{project.id}",
            method="PATCH",
            body=project.dict(),
        )

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot):
        raise NotImplementedError  # todo: snapshot api

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        raise NotImplementedError  # todo: snapshot api

    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        projects = self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[ProjectModel])
        return [Project(p, _RemoteProjectDashboard(p.id, self), self) for p in projects]

    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str],
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        raise NotImplementedError("Adding datasets is not supported yet")

    def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        self._request(f"/api/v2/dashboards/{project_id}", method="POST", body=dashboard.dict())

    def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        data = self._request(f"/api/v2/dashboards/{project_id}", method="GET", response_model=DashboardModel)
        return data


class CloudWorkspace(RemoteWorkspace):
    URL: str = "https://app.evidently.cloud"

    def __init__(
        self,
        token: Optional[str] = None,
        url: str = None,
    ):
        if token is None:
            token = os.environ.get("EVIDENTLY_API_KEY", default=None)
        if token is None:
            raise ValueError(
                "To use CloudWorkspace you must provide a token through argument or env variable EVIDENTLY_API_KEY"
            )
        self.token = token
        self.token_cookie_name = ACCESS_TOKEN_COOKIE.key
        self._jwt_token: Optional[str] = None
        self._logged_in: bool = False
        super().__init__(base_url=url if url is not None else self.URL)

    def _get_jwt_token(self):
        return super()._request("/api/users/login", "GET", headers={TOKEN_HEADER_NAME: self.token}).text

    @property
    def jwt_token(self):
        if self._jwt_token is None:
            self._jwt_token = self._get_jwt_token()

        return self._jwt_token

    def _prepare_request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ):
        r = super()._prepare_request(
            path=path,
            method=method,
            query_params=query_params,
            body=body,
            cookies=cookies,
            headers=headers,
            form_data=form_data,
        )
        if path == "/api/users/login":
            return r
        r.cookies[self.token_cookie_name] = self.jwt_token
        return r

    @overload
    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Type[T] = ...,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> T:
        pass

    @overload
    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Literal[None] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> Response:
        pass

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Optional[Type[T]] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> Union[Response, T]:
        try:
            res = super()._request(
                path=path,
                method=method,
                query_params=query_params,
                body=body,
                response_model=response_model,
                cookies=cookies,
                headers=headers,
                form_data=form_data,
            )
            self._logged_in = True
            return res
        except HTTPError as e:
            if self._logged_in and e.response.status_code == 401:
                # renew token and retry
                self._jwt_token = self._get_jwt_token()
                cookies[self.token_cookie_name] = self.jwt_token
                return super()._request(
                    path,
                    method,
                    query_params,
                    body,
                    response_model,
                    cookies=cookies,
                    headers=headers,
                    form_data=form_data,
                )
            raise

    def create_org(self, name: str) -> Org:
        return self._request("/api/orgs", "POST", body=Org(name=name).dict(), response_model=OrgModel).to_org()

    def list_orgs(self) -> List[Org]:
        return [o.to_org() for o in self._request("/api/orgs", "GET", response_model=List[OrgModel])]

    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str],
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        data_definition = dataset.data_definition.json()
        file = NamedBytesIO(b"", "data.parquet")
        dataset.as_dataframe().to_parquet(file)
        file.seek(0)
        qp = {"project_id": project_id}
        if link is not None:
            qp["snapshot_id"] = link.snapshot_id
            qp["dataset_type"] = link.dataset_type
            qp["dataset_subtype"] = link.dataset_subtype
        response: Response = self._request(
            "/api/v2/datasets/upload",
            "POST",
            body={
                "name": name,
                "description": description,
                "file": file,
                "data_definition_str": data_definition,
            },
            query_params=qp,
            form_data=True,
        )
        return DatasetID(response.json()["dataset"]["id"])

    def load_dataset(self, dataset_id: DatasetID) -> Dataset:
        response: Response = self._request(f"/api/v2/datasets/{dataset_id}/download", "GET")

        metadata, file_content = read_multipart_response(response)

        df = pd.read_parquet(io.BytesIO(file_content))
        data_def = parse_obj_as(DataDefinition, metadata["data_definition"])
        return Dataset.from_pandas(df, data_definition=data_def)

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot) -> SnapshotID:
        data = snapshot.dump_dict()
        resp: Response = self._request(f"/api/v2/snapshots/{project_id}", method="POST", body=data)
        return uuid.UUID(resp.json()["snapshot_id"])
