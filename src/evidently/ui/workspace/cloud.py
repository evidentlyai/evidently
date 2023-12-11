from typing import Optional
from uuid import UUID

from evidently._pydantic_compat import PrivateAttr
from evidently.ui.base import ProjectManager
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.workspace.remote import NoopBlobStorage
from evidently.ui.workspace.remote import NoopDataStorage
from evidently.ui.workspace.remote import RemoteMetadataStorage
from evidently.ui.workspace.view import WorkspaceView


class CloudMetadataStorage(RemoteMetadataStorage):
    token: str
    cookie_name: str
    _jwt_token: str = PrivateAttr(None)

    def _get_jwt_token(self):
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
    token: str

    URL: str = "https://cloud.evidentlyai.com"

    def __init__(self, token: str,
                 team_id: Optional[STR_UUID] = None, url: str = None):

        self.token = token
        self.url = url or self.URL

        meta = CloudMetadataStorage(base_url=self.url, token=self.token,
                                    cookie_name="app.at", )

        pm = ProjectManager(
            metadata=meta,
            blob=(NoopBlobStorage()),
            data=(NoopDataStorage()),
            auth=(NoopAuthManager())
        )
        super().__init__(None, pm, UUID(team_id) if isinstance(team_id, str) else team_id)
