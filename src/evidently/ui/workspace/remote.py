import contextlib
import datetime
import io
import json
import urllib.parse
import uuid
from typing import List
from typing import Optional
from typing import Set
from urllib.error import HTTPError

import requests
from pydantic import parse_obj_as

from evidently.suite.base_suite import Snapshot
from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import MetadataStorage
from evidently.ui.base import Project
from evidently.ui.base import ProjectManager
from evidently.ui.base import SnapshotMetadata
from evidently.ui.base import Team
from evidently.ui.base import User
from evidently.ui.dashboard.base import PanelValue
from evidently.ui.dashboard.base import ReportFilter
from evidently.ui.storage.common import NO_USER
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.type_aliases import BlobID
from evidently.ui.type_aliases import DataPoints
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import SnapshotID
from evidently.ui.workspace.view import WorkspaceView
from evidently.utils import NumpyEncoder


class RemoteMetadataStorage(MetadataStorage):
    base_url: str

    def _request(
            self,
            path: str,
            method: str,
            query_params: Optional[dict] = None,
            body: Optional[dict] = None,
            response_model=None,
            cookies=None
    ):
        # todo: better encoding
        headers = {}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"

            data = json.dumps(body, allow_nan=True, cls=NumpyEncoder).encode("utf8")

        response = requests.request(
            method, urllib.parse.urljoin(self.base_url, path), params=query_params, data=data, headers=headers, cookies=cookies
        )
        response.raise_for_status()
        if response_model is not None:
            return parse_obj_as(response_model, response.json())
        return response

    def add_project(self, project: Project, user: User, team: Team) -> Project:
        params = {}
        if team is not None and team.id is not None:
            params["team_id"] = str(team.id)
        return self._request("/api/projects/", "POST", query_params=params, body=project.dict(), response_model=Project)

    def get_project(self, project_id: uuid.UUID) -> Optional[Project]:
        try:
            return self._request(f"/api/projects/{project_id}/info", "GET", response_model=Project)
        except (HTTPError,) as e:
            try:
                data = e.response.json()  # type: ignore[attr-defined]
                if "detail" in data and data["detail"] == "project not found":
                    return None
                raise e
            except (ValueError, AttributeError):
                raise e

    def delete_project(self, project_id: ProjectID):
        return self._request(f"/api/projects/{project_id}", "DELETE")

    def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        return self._request("/api/projects", "GET", response_model=List[Project])

    def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot, blob_id: str):
        return self._request(f"/api/projects/{project_id}/snapshots", "POST", body=snapshot.dict())

    def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        return self._request(f"/api/projects/{project_id}/{snapshot_id}", "DELETE")

    def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        return [
            p.bind(self, NO_USER.id)
            for p in self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[Project])
        ]

    def list_snapshots(self, project_id: ProjectID, include_reports: bool = True, include_test_suites: bool = True) -> List[SnapshotMetadata]:
        raise NotImplementedError

    def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadata:
        raise NotImplementedError

    def update_project(self, project: Project) -> Project:
        return self._request(f"/api/projects/{project.id}/info", "POST", body=project.dict(), response_model=Project)


class NoopBlobStorage(BlobStorage):
    @contextlib.contextmanager
    def open_blob(self, id: BlobID):
        yield io.BytesIO(b"")

    def put_blob(self, path: str, obj):
        pass

    def get_snapshot_blob_id(self, project_id: ProjectID, snapshot: Snapshot) -> BlobID:
        pass


class NoopDataStorage(DataStorage):

    def extract_points(self, project_id: ProjectID, snapshot: Snapshot):
        pass

    def load_points(self, project_id: ProjectID, filter: ReportFilter, values: List["PanelValue"],
                    timestamp_start: Optional[datetime.datetime],
                    timestamp_end: Optional[datetime.datetime]) -> DataPoints:
        return []


class RemoteWorkspaceView(WorkspaceView):
    def verify(self):
        try:
            self.project_manager.metadata._request("/api/version", "GET").raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def __init__(self, base_url: str):
        self.base_url = base_url
        pm = ProjectManager(
            metadata=(RemoteMetadataStorage(base_url=self.base_url)),
            blob=(NoopBlobStorage()),
            data=(NoopDataStorage()),
            auth=(NoopAuthManager())
        )
        super().__init__(None, pm)
        self.verify()

    @classmethod
    def create(cls, base_url: str):
        return RemoteWorkspaceView(base_url)


RemoteWorkspace = RemoteWorkspaceView
