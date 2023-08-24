import pandas as pd

from evidently.collector.config import CollectorConfig
from evidently.ui.utils import RemoteClientBase


class CollectorClient(RemoteClientBase):
    def create_collector(self, id: str, collector: CollectorConfig):
        self._request(f"/{id}", "POST", body=collector.dict())

    def send_data(self, id: str, data: pd.DataFrame):
        self._request(f"/{id}/data", "POST", body=data.to_dict())

    def set_reference(self, id: str, reference: pd.DataFrame):
        self._request(f"/{id}/reference", "POST", body=reference.to_dict())
