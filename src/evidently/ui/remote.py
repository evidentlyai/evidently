import uuid
from json.decoder import JSONDecodeError
from typing import List
from typing import Optional
from typing import Union
from urllib.error import HTTPError

from evidently.suite.base_suite import Snapshot
from evidently.ui.dashboards import DashboardConfig
from evidently.ui.utils import RemoteClientBase
from evidently.ui.workspace import STR_UUID
from evidently.ui.workspace import ProjectBase
from evidently.ui.workspace import WorkspaceBase


class RemoteProject(ProjectBase["RemoteWorkspace"]):
    def save(self):
        self.workspace.add_project(self)


class RemoteWorkspace(RemoteClientBase, WorkspaceBase[RemoteProject]):
    def __init__(self, base_url: str, secret: str = None):
        super().__init__(base_url, secret)
        self.verify()

    def verify(self):
        try:
            response = self._request("/api/version", "GET")
            assert response.json()["application"] == "Evidently UI"
        except (HTTPError, JSONDecodeError, KeyError, AssertionError) as e:
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def create_project(self, name: str, description: Optional[str] = None) -> RemoteProject:
        project: ProjectBase = ProjectBase(
            name=name, description=description, dashboard=DashboardConfig(name=name, panels=[])
        )
        return self.add_project(project)

    def add_project(self, project: ProjectBase):
        return self._request("/api/projects", "POST", body=project.dict(), response_model=RemoteProject).bind(self)

    def get_project(self, project_id: uuid.UUID) -> RemoteProject:
        return self._request(f"/api/projects/{project_id}", "GET", response_model=RemoteProject)

    def delete_project(self, project_id: STR_UUID):
        return self._request(f"/api/projects/{project_id}", "DELETE")

    def list_projects(self) -> List[RemoteProject]:
        return self._request("/api/projects", "GET", response_model=List[RemoteProject])

    def add_snapshot(self, project_id: Union[str, uuid.UUID], snapshot: Snapshot):
        return self._request(f"/api/projects/{project_id}/snapshots", "POST", body=snapshot.dict())

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        return self._request(f"/api/projects/{project_id}/{snapshot_id}", "DELETE")

    def search_project(self, project_name: str) -> List[RemoteProject]:
        return [
            p.bind(self)
            for p in self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[RemoteProject])
        ]
