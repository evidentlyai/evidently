import json
import urllib.parse
import uuid
from typing import List
from typing import Optional
from typing import Union
from urllib.error import HTTPError

import requests

from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.ui.workspace import Project
from evidently.ui.workspace import WorkspaceBase
from evidently.utils import NumpyEncoder


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

    def add_report(self, project_id: Union[str, uuid.UUID], report: Report):
        return self._request(f"/api/projects/{project_id}/reports", "POST", body=report._get_payload().dict())

    def add_test_suite(self, project_id: Union[str, uuid.UUID], test_suite: TestSuite):
        return self._request(f"/api/projects/{project_id}/test_suites", "POST", body=test_suite._get_payload().dict())

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        raise NotImplementedError

    def get_project(self, project_id: uuid.UUID) -> Project:
        raise NotImplementedError

    def list_projects(self) -> List[Project]:
        raise NotImplementedError
