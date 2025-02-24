import dataclasses
import json
from io import BytesIO
from typing import BinaryIO
from typing import Dict
from typing import List
from typing import Literal
from typing import NamedTuple
from typing import Optional
from typing import Type
from typing import Union
from typing import overload

import pandas as pd
from requests import HTTPError
from requests import Response

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pydantic_utils import get_classpath
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.ui.api.models import OrgModel
from evidently.ui.api.models import TeamModel
from evidently.ui.base import Org
from evidently.ui.base import Team
from evidently.ui.datasets import DatasetSourceType
from evidently.ui.managers.projects import ProjectManager
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.type_aliases import ZERO_UUID
from evidently.ui.type_aliases import DatasetID
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import TeamID
from evidently.ui.workspace.remote import NoopBlobStorage
from evidently.ui.workspace.remote import NoopDataStorage
from evidently.ui.workspace.remote import RemoteProjectMetadataStorage
from evidently.ui.workspace.remote import T
from evidently.ui.workspace.view import WorkspaceView

TOKEN_HEADER_NAME = "X-Evidently-Token"


class Cookie(NamedTuple):
    key: str
    description: str
    httponly: bool


ACCESS_TOKEN_COOKIE = Cookie(
    key="app.at",
    description="",
    httponly=True,
)


class CloudMetadataStorage(RemoteProjectMetadataStorage):
    def __init__(self, base_url: str, token: str, token_cookie_name: str):
        self.token = token
        self.token_cookie_name = token_cookie_name
        self._jwt_token: Optional[str] = None
        self._logged_in: bool = False
        super().__init__(base_url=base_url)

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

    def create_org(self, org: Org) -> OrgModel:
        return self._request("/api/orgs", "POST", body=org.dict(), response_model=OrgModel)

    def list_orgs(self) -> List[OrgModel]:
        return self._request("/api/orgs", "GET", response_model=List[OrgModel])

    def create_team(self, team: Team, org_id: OrgID = None) -> TeamModel:
        return self._request(
            "/api/teams",
            "POST",
            query_params={"name": team.name, "org_id": org_id},
            response_model=TeamModel,
        )

    def add_dataset(
        self,
        file: BinaryIO,
        name: str,
        project_id: ProjectID,
        description: Optional[str],
        column_mapping: Optional[ColumnMapping],
        dataset_source: DatasetSourceType = DatasetSourceType.file,
    ) -> DatasetID:
        cm_payload = json.dumps(dataclasses.asdict(column_mapping)) if column_mapping is not None else None
        response: Response = self._request(
            "/api/datasets/",
            "POST",
            body={
                "name": name,
                "description": description,
                "file": file,
                "column_mapping": cm_payload,
                "source_type": dataset_source.value,
            },
            query_params={"project_id": project_id},
            form_data=True,
        )
        return DatasetID(response.json()["dataset_id"])

    def load_dataset(self, dataset_id: DatasetID) -> pd.DataFrame:
        response: Response = self._request(f"/api/datasets/{dataset_id}/download", "GET")
        return pd.read_parquet(BytesIO(response.content))


class NamedBytesIO(BytesIO):
    def __init__(self, initial_bytes: bytes, name: str):
        super().__init__(initial_bytes=initial_bytes)
        self.name = name


class CloudWorkspace(WorkspaceView):
    token: str
    URL: str = "https://app.evidently.cloud"

    def __init__(
        self,
        token: str,
        url: str = None,
    ):
        self.token = token
        self.url = url if url is not None else self.URL

        # todo: default org if user have only one
        user_id = ZERO_UUID  # todo: get from /me
        meta = CloudMetadataStorage(
            base_url=self.url,
            token=self.token,
            token_cookie_name=ACCESS_TOKEN_COOKIE.key,
        )

        pm = ProjectManager(
            project_metadata=meta,
            blob_storage=(NoopBlobStorage()),
            data_storage=(NoopDataStorage()),
            auth_manager=(CloudAuthManager()),
        )
        super().__init__(
            user_id,
            pm,
        )

    def create_org(self, name: str) -> Org:
        assert isinstance(self.project_manager.project_metadata, CloudMetadataStorage)
        return self.project_manager.project_metadata.create_org(Org(name=name)).to_org()

    def list_orgs(self) -> List[Org]:
        assert isinstance(self.project_manager.project_metadata, CloudMetadataStorage)
        return [o.to_org() for o in self.project_manager.project_metadata.list_orgs()]

    def create_team(self, name: str, org_id: OrgID) -> Team:
        assert isinstance(self.project_manager.project_metadata, CloudMetadataStorage)
        return self.project_manager.project_metadata.create_team(Team(name=name, org_id=org_id), org_id).to_team()

    def add_dataset(
        self,
        data_or_path: Union[str, pd.DataFrame],
        name: str,
        project_id: STR_UUID,
        description: Optional[str] = None,
        column_mapping: Optional[ColumnMapping] = None,
        dataset_source: DatasetSourceType = DatasetSourceType.file,
    ) -> DatasetID:
        file: Union[NamedBytesIO, BinaryIO]
        assert isinstance(self.project_manager.project_metadata, CloudMetadataStorage)
        if isinstance(data_or_path, str):
            file = open(data_or_path, "rb")
        elif isinstance(data_or_path, pd.DataFrame):
            file = NamedBytesIO(b"", "data.parquet")
            data_or_path.to_parquet(file)
            file.seek(0)
        else:
            raise NotImplementedError(f"Add datasets is not implemented for {get_classpath(data_or_path.__class__)}")
        if isinstance(project_id, str):
            project_id = ProjectID(project_id)
        try:
            return self.project_manager.project_metadata.add_dataset(
                file, name, project_id, description, column_mapping, dataset_source
            )
        finally:
            file.close()

    def load_dataset(self, dataset_id: DatasetID) -> pd.DataFrame:
        assert isinstance(self.project_manager.project_metadata, CloudMetadataStorage)
        return self.project_manager.project_metadata.load_dataset(dataset_id)

    def add_report_with_data(self, project_id: STR_UUID, report: Report):
        self.add_report(project_id, report)

    def add_test_suite_with_data(self, project_id: STR_UUID, test_suite: TestSuite):
        self.add_test_suite(project_id, test_suite)


class CloudAuthManager(NoopAuthManager):
    async def get_team(self, team_id: TeamID) -> Optional[Team]:
        return Team(id=team_id, name="", org_id=ZERO_UUID)
