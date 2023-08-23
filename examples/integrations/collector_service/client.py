import json
from typing import Optional

import pandas as pd
import requests
import urllib.parse
from pydantic import BaseModel, parse_obj_as

from evidently.utils import NumpyEncoder
from examples.integrations.collector_service.config import CollectorConfig


class CollectorClient(BaseModel):
    # todo: unify with RemoteWorkspace
    base_url: str = "http://localhost:8081"
    secret: Optional[str] = None

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

    def create_collector(self, id: str, collector: CollectorConfig):
        self._request(f"/{id}", "POST", body=collector.dict())

    def send_data(self, id: str, data: pd.DataFrame):
        self._request(f"/{id}/data", "POST", body=data.to_dict())

    def set_reference(self, id: str, reference: pd.DataFrame):
        self._request(f"/{id}/reference", "POST", body=reference.to_dict())
