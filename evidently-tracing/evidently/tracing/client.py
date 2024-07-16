import urllib.parse
from typing import Optional

import requests


class EvidentlyCloudClient:
    _cookie_key: str = "app.at"

    def __init__(self, url: str, token: str):
        self._base_url = url
        self._token = token
        self._session = requests.Session()
        self._jwt_token = None

        def refresh_token(r, *args, **kwargs):
            if r.status_code == 401:
                self._jwt_token = None
                self._session.headers.update({"Authorization": f"Bearer {self.jwt_token()}"})
                r.request.headers["Authorization"] = self._session.headers["Authorization"]
                return self._session.send(r.request)

        self._session.hooks["response"].append(refresh_token)

    def request(
        self,
        path: str,
        method: str,
        headers: Optional[dict] = None,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> requests.Response:
        url = urllib.parse.urljoin(self._base_url, path)
        req = requests.Request(method, url, params=query_params, headers=headers, json=body)
        if path != "/api/users/login":
            req.headers["Authorization"] = f"Bearer {self.jwt_token()}"
        resp = self.session().send(req.prepare())
        resp.raise_for_status()
        return resp

    def session(self) -> requests.Session:
        return self._session

    def jwt_token(self) -> str:
        if self._jwt_token is None:
            self._jwt_token = self.request(
                "/api/users/login",
                "GET",
                headers={"X-Evidently-Token": self._token},
            ).text
        return self._jwt_token
