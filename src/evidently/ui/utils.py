import json
import os
import urllib.parse
from typing import Optional

import requests
from fastapi import Header
from fastapi import HTTPException
from typing_extensions import Annotated

from evidently._pydantic_compat import parse_obj_as
from evidently.utils import NumpyEncoder

SECRET = os.environ.get("EVIDENTLY_SECRET", None)


def set_secret(secret: Optional[str]):
    global SECRET
    SECRET = secret


async def authenticated(evidently_secret: Annotated[Optional[str], Header()] = None):
    if SECRET is not None and evidently_secret != SECRET:
        raise HTTPException(403, "Not allowed")


class RemoteClientBase:
    def __init__(self, base_url: str, secret: str = None):
        self.base_url = base_url
        self.secret = secret

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model=None,
    ):
        # todo: better encoding
        headers = {"evidently-secret": self.secret}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"

            data = json.dumps(body, allow_nan=True, cls=NumpyEncoder).encode("utf8")

        response = requests.request(
            method, urllib.parse.urljoin(self.base_url, path), params=query_params, data=data, headers=headers
        )
        response.raise_for_status()
        if response_model is not None:
            return parse_obj_as(response_model, response.json())
        return response
