import contextlib
import datetime
import io
import json
import urllib.parse
from json import JSONDecodeError
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload
from urllib.error import HTTPError

from requests import Request
from requests import Response
from requests import Session

from evidently._pydantic_compat import parse_obj_as
from evidently.errors import EvidentlyError
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.ui.api.service import EVIDENTLY_APPLICATION_NAME
from evidently.legacy.ui.base import BlobMetadata
from evidently.legacy.ui.base import BlobStorage
from evidently.legacy.ui.base import DataStorage
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.base import ProjectMetadataStorage
from evidently.legacy.ui.base import SnapshotMetadata
from evidently.legacy.ui.base import Team
from evidently.legacy.ui.base import User
from evidently.legacy.ui.dashboards.base import PanelValue
from evidently.legacy.ui.dashboards.base import ReportFilter
from evidently.legacy.ui.dashboards.test_suites import TestFilter
from evidently.legacy.ui.errors import ProjectNotFound
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.storage.common import SECRET_HEADER_NAME
from evidently.legacy.ui.storage.common import NoopAuthManager
from evidently.legacy.ui.type_aliases import ZERO_UUID
from evidently.legacy.ui.type_aliases import BlobID
from evidently.legacy.ui.type_aliases import DataPointsAsType
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PointType
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TestResultPoints
from evidently.legacy.ui.workspace.view import WorkspaceView
from evidently.legacy.utils import NumpyEncoder

T = TypeVar("T")


class RemoteBase:
    def get_url(self):
        raise NotImplementedError

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
        # todo: better encoding
        cookies = cookies or {}
        headers = headers or {}
        data: Optional[Union[Dict, bytes]] = None
        files = None
        if body is not None:
            if form_data:
                data = body
                files = {k: body.pop(k) for k in list(body.keys()) if isinstance(body[k], io.IOBase)}
            else:
                headers["Content-Type"] = "application/json"
                data = json.dumps(body, allow_nan=True, cls=NumpyEncoder).encode("utf8")
        return Request(
            method,
            urllib.parse.urljoin(self.get_url(), path),
            params=query_params,
            data=data,
            files=files,
            headers=headers,
            cookies=cookies,
        )

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
        request = self._prepare_request(path, method, query_params, body, cookies, headers, form_data=form_data)
        s = Session()
        response = s.send(request.prepare())

        if response.status_code >= 400:
            try:
                details = response.json()["detail"]
                raise EvidentlyError(details)
            except ValueError:
                pass
        response.raise_for_status()
        if response_model is not None:
            return parse_obj_as(response_model, response.json())
        return response


class RemoteProjectMetadataStorage(ProjectMetadataStorage, RemoteBase):
    def __init__(self, base_url: str, secret: Optional[str] = None):
        self.base_url = base_url
        self.secret = secret

    def get_url(self):
        return self.base_url

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

    async def add_project(
        self, project: Project, user: User, team: Optional[Team], org_id: Optional[OrgID] = None
    ) -> Project:
        params = {}
        if team is not None and team.id is not None and team.id != ZERO_UUID:
            params["team_id"] = str(team.id) if team is not None else None
        if org_id:
            params["org_id"] = str(org_id)
        return self._request("/api/projects", "POST", query_params=params, body=project.dict(), response_model=Project)

    async def get_project(self, project_id: ProjectID) -> Optional[Project]:
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

    async def delete_project(self, project_id: ProjectID):
        return self._request(f"/api/projects/{project_id}", "DELETE")

    async def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        return self._request("/api/projects", "GET", response_model=List[Project])

    async def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot, blob: "BlobMetadata"):
        return self._request(f"/api/projects/{project_id}/snapshots", "POST", body=snapshot.dict())

    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        return self._request(f"/api/projects/{project_id}/{snapshot_id}", "DELETE")

    async def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        return self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[Project])

    async def list_snapshots(
        self, project_id: ProjectID, include_reports: bool = True, include_test_suites: bool = True
    ) -> List[SnapshotMetadata]:
        project = await self.get_project(project_id)
        if project is None:
            raise ProjectNotFound()
        return [
            sm.bind(project)
            for sm in self._request(
                f"/api/projects/{project_id}/snapshots", "GET", response_model=List[SnapshotMetadata]
            )
        ]

    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadata:
        project = await self.get_project(project_id)
        if project is None:
            raise ProjectNotFound()
        return self._request(
            f"/api/projects/{project_id}/{snapshot_id}/metadata", "GET", response_model=SnapshotMetadata
        ).bind(project)

    async def update_project(self, project: Project) -> Project:
        return self._request(f"/api/projects/{project.id}/info", "POST", body=project.dict(), response_model=Project)

    async def reload_snapshots(self, project_id: ProjectID):
        self._request(f"/api/projects/{project_id}/reload", "GET")


class NoopBlobStorage(BlobStorage):
    @contextlib.contextmanager
    def open_blob(self, id: BlobID):
        yield io.BytesIO(b"")

    async def put_blob(self, path: str, obj):
        pass

    def get_snapshot_blob_id(self, project_id: ProjectID, snapshot: Snapshot) -> BlobID:
        return ""

    async def get_blob_metadata(self, blob_id: BlobID) -> BlobMetadata:
        return BlobMetadata(id=blob_id, size=0)


class NoopDataStorage(DataStorage):
    async def extract_points(self, project_id: ProjectID, snapshot: Snapshot):
        pass

    async def load_test_results(
        self,
        project_id: ProjectID,
        filter: ReportFilter,
        test_filters: List[TestFilter],
        time_agg: Optional[str],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> TestResultPoints:
        return {}

    async def load_points_as_type(
        self,
        cls: Type[PointType],
        project_id: ProjectID,
        filter: "ReportFilter",
        values: List["PanelValue"],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DataPointsAsType[PointType]:
        return []


class RemoteWorkspaceView(WorkspaceView):
    def verify(self):
        try:
            response = self.project_manager.project_metadata._request("/api/version", "GET")
            assert response.json()["application"] == EVIDENTLY_APPLICATION_NAME
        except (HTTPError, JSONDecodeError, KeyError, AssertionError) as e:
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def __init__(self, base_url: str, secret: Optional[str] = None):
        self.base_url = base_url
        self.secret = secret
        pm = ProjectManager(
            project_metadata=(RemoteProjectMetadataStorage(base_url=self.base_url, secret=self.secret)),
            blob_storage=(NoopBlobStorage()),
            data_storage=(NoopDataStorage()),
            auth_manager=(NoopAuthManager()),
        )
        super().__init__(None, pm)
        self.verify()

    @classmethod
    def create(cls, base_url: str):
        return RemoteWorkspaceView(base_url)


RemoteWorkspace = RemoteWorkspaceView
