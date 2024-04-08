from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from uuid import UUID

from requests import HTTPError

from evidently._pydantic_compat import PrivateAttr
from evidently.ui.api.models import OrgModel
from evidently.ui.base import Org
from evidently.ui.base import ProjectManager
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.type_aliases import ZERO_UUID
from evidently.ui.type_aliases import OrgID
from evidently.ui.workspace.remote import NoopBlobStorage
from evidently.ui.workspace.remote import NoopDataStorage
from evidently.ui.workspace.remote import RemoteMetadataStorage
from evidently.ui.workspace.view import WorkspaceView

TOKEN_HEADER_NAME = "X-Evidently-Token"


class Cookie(NamedTuple):
    key: str
    description: str
    httponly: bool


ORG_ID_COOKIE = Cookie(
    key="org-id",
    description="We use this cookie to identify the organization",
    # we set `httponly=False` to be able to read it in the UI
    httponly=False,
)

ACCESS_TOKEN_COOKIE = Cookie(
    key="app.at",
    description="",
    httponly=True,
)


class CloudMetadataStorage(RemoteMetadataStorage):
    token: str
    token_cookie_name: str
    org_id: OrgID
    org_id_cookie_name: str

    _jwt_token: str = PrivateAttr(None)
    _logged_in: bool = PrivateAttr(False)

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
    ):
        r = super()._prepare_request(path, method, query_params, body, cookies, headers)
        if path == "/api/users/login":
            return r
        r.cookies[self.token_cookie_name] = self.jwt_token
        r.cookies[self.org_id_cookie_name] = str(self.org_id)
        return r

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model=None,
        cookies=None,
        headers: Dict[str, str] = None,
    ):
        try:
            res = super()._request(
                path,
                method,
                query_params,
                body,
                response_model,
                cookies=cookies,
                headers=headers,
            )
            self._logged_in = True
            return res
        except HTTPError as e:
            if self._logged_in and e.response.status_code == 401:
                # renew token and retry
                self._jwt_token = self._get_jwt_token()
                cookies[self.cookie_name] = self.jwt_token
                return super()._request(
                    path,
                    method,
                    query_params,
                    body,
                    response_model,
                    cookies=cookies,
                    headers=headers,
                )
            raise

    def switch_org(self, org_id: OrgID):
        self.org_id = org_id

    def create_org(self, org: Org) -> OrgModel:
        return self._request("/api/orgs", "POST", body=org.dict(), response_model=OrgModel)

    def list_orgs(self) -> List[OrgModel]:
        return self._request("/api/orgs", "GET", response_model=List[OrgModel])


class CloudWorkspace(WorkspaceView):
    token: str
    URL: str = "https://app.evidently.cloud"

    def __init__(
        self,
        token: str,
        org_id: STR_UUID,
        team_id: Optional[STR_UUID] = None,
        url: str = None,
    ):
        self.token = token
        self.url = url if url is not None else self.URL

        # todo: default org if user have only one
        org_id_uuid = UUID(org_id) if isinstance(org_id, str) else org_id
        user_id = ZERO_UUID  # todo: get from /me
        meta = CloudMetadataStorage(
            base_url=self.url,
            token=self.token,
            token_cookie_name=ACCESS_TOKEN_COOKIE.key,
            org_id=org_id or ZERO_UUID,
            org_id_cookie_name=ORG_ID_COOKIE.key,
        )

        pm = ProjectManager(
            metadata=meta,
            blob=(NoopBlobStorage()),
            data=(NoopDataStorage()),
            auth=(NoopAuthManager()),
        )
        super().__init__(
            user_id,
            pm,
            UUID(team_id) if isinstance(team_id, str) else team_id,
            org_id_uuid,
        )

    def switch_org(self, org_id: STR_UUID):
        org_id_uuid = UUID(org_id) if isinstance(org_id, str) else org_id
        assert isinstance(self.project_manager.metadata, CloudMetadataStorage)
        self.project_manager.metadata.switch_org(org_id_uuid)

    def create_org(self, org: Org) -> OrgModel:
        assert isinstance(self.project_manager.metadata, CloudMetadataStorage)
        return self.project_manager.metadata.create_org(org)

    def list_orgs(self) -> List[OrgModel]:
        assert isinstance(self.project_manager.metadata, CloudMetadataStorage)
        return self.project_manager.metadata.list_orgs()
