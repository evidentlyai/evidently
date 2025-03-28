import io
import os
import uuid
from abc import ABC
from abc import abstractmethod
from json import JSONDecodeError
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Type
from typing import Union
from typing import overload

import pandas as pd
from requests import HTTPError
from requests import Response

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import parse_obj_as
from evidently.future.datasets import DataDefinition
from evidently.future.datasets import Dataset
from evidently.future.report import Snapshot
from evidently.ui.api.models import OrgModel
from evidently.ui.api.service import EVIDENTLY_APPLICATION_NAME
from evidently.ui.base import Org
from evidently.ui.base import Project
from evidently.ui.dashboards import DashboardConfig
from evidently.ui.storage.common import SECRET_HEADER_NAME
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.type_aliases import DatasetID
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import SnapshotID
from evidently.ui.workspace.cloud import ACCESS_TOKEN_COOKIE
from evidently.ui.workspace.cloud import TOKEN_HEADER_NAME
from evidently.ui.workspace.cloud import NamedBytesIO
from evidently.ui.workspace.cloud import read_multipart_response
from evidently.ui.workspace.remote import RemoteBase
from evidently.ui.workspace.remote import T


class ProjectV2(Project):
    _workspace: Optional["WorkspaceBase"] = PrivateAttr(None)

    def bind_workspace(self, ws: "WorkspaceBase") -> "ProjectV2":
        self._workspace = ws
        return self


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
            Project(
                name=name,
                description=description,
                dashboard=DashboardConfig(name=name, panels=[]),
                org_id=org_id,
            ),
            org_id,
        )
        return project

    @abstractmethod
    def add_project(self, project: Project, org_id: Optional[OrgID] = None) -> Project:
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
            raise ValueError(f"Evidenly API not available at {self.base_url}") from e

    def __init__(self, base_url: str, secret: Optional[str] = None):
        self.base_url = base_url
        self.secret = secret
        self.verify()

    @classmethod
    def create(cls, base_url: str):
        return RemoteWorkspace(base_url)

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

    def add_project(self, project: Project, org_id: Optional[OrgID] = None) -> Project:
        params = {}
        if org_id:
            params["org_id"] = str(org_id)
        project_id = self._request(
            "/api/v2/projects", "POST", query_params=params, body=project.dict(), response_model=ProjectID
        )
        p = self.get_project(project_id)
        assert p is not None
        return p

    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        try:
            return self._request(f"/api/projects/{project_id}/info", "GET", response_model=ProjectV2).bind_workspace(
                self
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
        projects = self._request("/api/v2/projects", "GET", response_model=List[ProjectV2])
        return [p.bind_workspace(self) for p in projects]

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot):
        raise NotImplementedError  # todo: snapshot api

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        raise NotImplementedError  # todo: snapshot api

    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        projects = self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[ProjectV2])
        return [p.bind_workspace(self) for p in projects]

    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str],
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        raise NotImplementedError("Adding datasets is not supported yet")


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

    def list_orgs(self) -> List[OrgModel]:
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
