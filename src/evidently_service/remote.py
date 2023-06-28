import json
import urllib.parse
import uuid
from typing import List
from typing import Optional
from typing import Union
from urllib.error import HTTPError

import requests

from evidently.report import Report
from evidently.suite.base_suite import Snapshot
from evidently.test_suite import TestSuite
from evidently.utils import NumpyEncoder
from evidently_service.workspace import Project
from evidently_service.workspace import WorkspaceBase


class RemoteWorkspace(WorkspaceBase):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.verify()

    def verify(self):
        try:
            self._request("/api", "GET").raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def _request(self, path: str, method: str, query_params: Optional[dict] = None, body: Optional[dict] = None):
        # todo: better encoding
        response = requests.request(
            method,
            urllib.parse.urljoin(self.base_url, path),
            params=query_params,
            json=json.loads(json.dumps(body, cls=NumpyEncoder)),
        )
        response.raise_for_status()
        return response

    def add_project(self, project: Project):
        return self._request("/api/projects", "POST", body=project.dict())

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        raise NotImplementedError

    def get_project(self, project_id: uuid.UUID) -> Project:
        raise NotImplementedError

    def list_projects(self) -> List[Project]:
        raise NotImplementedError

    def add_snapshot(self, project_id: Union[str, uuid.UUID], snapshot: Snapshot):
        return self._request(f"/api/projects/{project_id}/snapshots", "POST", body=snapshot.dict())

