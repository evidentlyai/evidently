import json
from typing import Optional
from typing import Union

from evidently import Dataset
from evidently.core.report import Snapshot
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.utils import NumpyEncoder
from evidently.ui.workspace import CloudWorkspace
from evidently.ui.workspace import RemoteWorkspace


class _URI:
    def __init__(self, uri: str):
        self.uri = uri
        if self.is_cloud or self.is_remote:
            self.ws = self._get_ws()

    def _get_ws(self) -> Union[RemoteWorkspace, CloudWorkspace]:
        if self.is_remote:
            proto, addr = self.uri.split("://", maxsplit=1)
            return RemoteWorkspace(f"{proto}://{addr.split('/')[0]}")
        if self.is_cloud:
            _, addr = self.uri.split("://", maxsplit=1)
            if len(addr.split("/")) > 1:
                base_url = "https://" + addr.split("/")[0]
            else:
                base_url = None
            return CloudWorkspace(url=base_url)
        raise ValueError(f"{self.uri} is not a valid remote or cloud URI")

    @property
    def is_cloud(self):
        return self.uri.startswith("cloud://")

    @property
    def is_remote(self):
        return self.uri.startswith("http")

    @property
    def is_local(self):
        return not self.is_cloud and not self.is_remote

    def load_dataset(self) -> Dataset:
        if self.is_local:
            # raise NotImplementedError("not yet implemented")
            return Dataset.load(self.uri)
        if self.is_remote:
            raise ValueError("Remote workspace does not support dataset loading")
        if self.is_cloud:
            return self.ws.load_dataset(DatasetID(self.uri.split("/")[-1]))
        raise ValueError(f"{self.uri} is not a valid dataset URI")

    def upload_snapshot(self, snapshot: Snapshot, include_datasets: bool):
        if self.is_local:
            with open(self.uri, "w") as f:
                f.write(json.dumps(snapshot.to_snapshot_model().dict(), indent=2, ensure_ascii=False, cls=NumpyEncoder))
            return
        if self.is_remote or self.is_cloud:
            self.ws.add_run(self.uri.split("/")[-1], snapshot, include_datasets)
            return
        raise ValueError(f"{self.uri} is not a valid URI")

    def upload_dataset(self, dataset: Dataset, name: Optional[str]):
        if self.is_local:
            dataset.save(self.uri)
            return
        if self.is_cloud:
            self.ws.add_dataset(ProjectID(self.uri.split("/")[-1]), dataset, name or "", None)
            return
        if self.is_remote:
            raise ValueError("Remote workspace does not support dataset uploading")
        raise ValueError(f"{self.uri} is not a valid URI")
