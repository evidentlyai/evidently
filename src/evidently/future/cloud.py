import uuid
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload

from requests import HTTPError
from requests import Response

from evidently.future.report import Snapshot
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import SnapshotID
from evidently.ui.workspace.cloud import ACCESS_TOKEN_COOKIE
from evidently.ui.workspace.cloud import TOKEN_HEADER_NAME
from evidently.ui.workspace.remote import RemoteBase

T = TypeVar("T")


class CloudClientBase(RemoteBase):
    _jwt_token: Optional[str] = None

    def __init__(
        self,
        base_url: str = "https://app.evidently.cloud",
        token: Optional[str] = None,
    ):
        self.base_url = base_url
        if token is None:
            import os

            token = os.environ.get("EVIDENTLY_API_KEY", default=None)
        if token is None:
            raise ValueError(
                "To use CloudWorkspace you must provide a token through argument or env variable EVIDENTLY_API_KEY"
            )
        self.token = token
        self._jwt_token = None

    def _get_jwt_token(self):
        return super()._request("/api/users/login", "GET", headers={TOKEN_HEADER_NAME: self.token}).text

    def get_url(self) -> str:
        return self.base_url

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
        r.cookies[ACCESS_TOKEN_COOKIE.key] = self.jwt_token
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
                cookies[ACCESS_TOKEN_COOKIE.key] = self.jwt_token
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


class CloudClient(CloudClientBase):
    def __init__(
        self,
        base_url: str = "https://app.evidently.cloud",
        token: Optional[str] = None,
    ):
        super().__init__(base_url, token)

    def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot) -> SnapshotID:
        data = snapshot.dump_dict()
        resp: Response = self._request(f"/api/v2/snapshots/{project_id}", method="POST", body=data)
        return uuid.UUID(resp.json()["snapshot_id"])
