from typing import Optional
from uuid import UUID

import requests
from pydantic import PrivateAttr
from requests.models import HTTPError

from evidently.ui.base import ProjectManager
from evidently.ui.errors import NotAuthorized
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.workspace.remote import NoopBlobStorage
from evidently.ui.workspace.remote import NoopDataStorage
from evidently.ui.workspace.remote import RemoteMetadataStorage
from evidently.ui.workspace.view import WorkspaceView


def get_jwt_token(fa_base_url, application_id, login: str, password: str, tenant: str):
    try:
        r = requests.post(fa_base_url + "/api/login", json={
            "loginId": login,
            "password": password,
            "applicationId": application_id,
        }, headers={"X-FusionAuth-TenantId": tenant})
        r.raise_for_status()
        return r.json()["token"]
    except HTTPError as e:
        if e.response.status_code in (401, 404):
            raise NotAuthorized()
        raise


class CloudMetadataStorage(RemoteMetadataStorage):
    username: Optional[str]
    password: Optional[str]
    token: Optional[str]

    cookie_name: str
    fa_url: str = "https://evidentlyai.fusionauth.io"
    application_id: str = "0ac7ba86-e545-4546-b422-db3fb712b787"
    tenant: str = "7917e57e-0ad4-4011-9b16-03602d034ef3"

    _jwt_token: str = PrivateAttr(None)

    def _get_jwt_token(self):
        if self.token is None:
            if self.username is None or self.password is None:
                raise ValueError("Both username and password should be provided")
            return get_jwt_token(self.fa_url, self.application_id, self.username, self.password, self.tenant)

        return super()._request("/api/users/login", "GET", query_params={"token": self.token}).text

    @property
    def jwt_token(self):
        if self._jwt_token is None:
            self._jwt_token = self._get_jwt_token()

        return self._jwt_token

    def _request(self, path: str, method: str, query_params: Optional[dict] = None, body: Optional[dict] = None, response_model=None,
                 cookies=None):
        cookies = cookies or {}
        cookies = cookies.copy()
        cookies[self.cookie_name] = self.jwt_token
        return super()._request(path, method, query_params, body, response_model, cookies=cookies)


class CloudWorkspace(WorkspaceView):
    username: Optional[str]
    password: Optional[str]
    token: Optional[str]

    URL: str = "https://cloud.evidentlyai.com"

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None, team_id: Optional[STR_UUID] = None, url: str = None):
        if token is None and username is None and password is None:
            raise ValueError("You should provide either token or username and password")
        self.username = username
        self.password = password
        self.token = token
        self.url = url or self.URL

        meta = CloudMetadataStorage(base_url=self.url, username=self.username, password=self.password, token=self.token,
                                    cookie_name="app.at", )

        pm = ProjectManager(
            metadata=meta,
            blob=(NoopBlobStorage()),
            data=(NoopDataStorage()),
            auth=(NoopAuthManager())
        )
        super().__init__(None, pm, UUID(team_id) if isinstance(team_id, str) else team_id)
