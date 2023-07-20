import json
import urllib.parse
import uuid
from typing import List
from typing import Optional
from typing import Union
from urllib.error import HTTPError

import requests
from pydantic import parse_obj_as

from evidently.suite.base_suite import Snapshot
from evidently.ui.dashboards import DashboardConfig
from evidently.ui.workspace import ProjectBase
from evidently.ui.workspace import WorkspaceBase
from evidently.utils import NumpyEncoder


class RemoteProject(ProjectBase["RemoteWorkspace"]):
    def save(self):
        self.workspace.add_project(self)


class RemoteWorkspace(WorkspaceBase[RemoteProject]):
    def __init__(self, base_url: str, secret: str = None):
        self.base_url = base_url
        self.secret = secret
        self.verify()

    def verify(self):
        try:
            self._request("/api", "GET").raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model=None,
    ):
        # todo: better encoding
        headers = {"evidently-secret": self.secret}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"

            data = json.dumps(body, allow_nan=True, cls=NumpyEncoder).encode("utf8")

        response = requests.request(
            method, urllib.parse.urljoin(self.base_url, path), params=query_params, data=data, headers=headers
        )
        response.raise_for_status()
        if response_model is not None:
            return parse_obj_as(response_model, response.json())
        return response

    def create_project(self, name: str, description: Optional[str] = None) -> RemoteProject:
        project: ProjectBase = ProjectBase(
            name=name, description=description, dashboard=DashboardConfig(name=name, panels=[])
        )
        return self.add_project(project)

    def add_project(self, project: ProjectBase):
        return self._request("/api/projects", "POST", body=project.dict(), response_model=RemoteProject).bind(self)

    def get_project(self, project_id: uuid.UUID) -> RemoteProject:
        return self._request(f"/api/projects/{project_id}", "GET", response_model=RemoteProject)

    def list_projects(self) -> List[RemoteProject]:
        return self._request("/api/projects", "GET", response_model=List[RemoteProject])

    def add_snapshot(self, project_id: Union[str, uuid.UUID], snapshot: Snapshot):
        return self._request(f"/api/projects/{project_id}/snapshots", "POST", body=snapshot.dict())

    def search_project(self, project_name: str) -> List[RemoteProject]:
        return [
            p.bind(self)
            for p in self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[RemoteProject])
        ]
