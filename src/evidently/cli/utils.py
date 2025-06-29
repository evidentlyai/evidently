import importlib.util
import json
import os.path
from importlib import import_module
from pathlib import Path
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from evidently import Dataset
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
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
            assert isinstance(self.ws, CloudWorkspace)
            return self.ws.load_dataset(DatasetID(self.uri.split("/")[-1]))
        raise ValueError(f"{self.uri} is not a valid dataset URI")

    def upload_snapshot(self, snapshot: Snapshot, include_datasets: bool):
        if self.is_local:
            with open(self.uri, "w") as f:
                f.write(json.dumps(snapshot.to_snapshot_model().dict(), indent=2, ensure_ascii=False, cls=NumpyEncoder))
            return self.uri
        if self.is_remote or self.is_cloud:
            project_id = self.uri.split("/")[-1]
            ref = self.ws.add_run(project_id, snapshot, include_datasets)
            return ref.url
        raise ValueError(f"{self.uri} is not a valid URI")

    def upload_dataset(self, dataset: Dataset, name: Optional[str]) -> str:
        if self.is_local:
            dataset.save(self.uri)
            return self.uri
        if self.is_cloud:
            project_id = ProjectID(self.uri.split("/")[-1])
            dataset_id = self.ws.add_dataset(project_id, dataset, name or "", None)
            return f"{self.ws.base_url}/v2/projects/{project_id}/datasets/{dataset_id}"
        if self.is_remote:
            raise ValueError("Remote workspace does not support dataset uploading")
        raise ValueError(f"{self.uri} is not a valid URI")


T = TypeVar("T", bound="_Config")


class _Config(BaseModel):
    @classmethod
    def load(cls: Type[T], path: str) -> "T":
        with open(path) as f:
            return parse_obj_as(cls, json.load(f))

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.json(indent=2, ensure_ascii=False))


def _load_config_from_python(config_type: Type[T], path_or_module: str) -> T:
    object_path: Optional[str]
    if ":" in path_or_module:
        path_or_module, object_path = path_or_module.split(":", 1)
    else:
        object_path = None
    if os.path.exists(path_or_module):
        path = Path(path_or_module)
        module_name = path.stem  # e.g. 'my_script' from 'my_script.py'
        spec = importlib.util.spec_from_file_location(module_name, path_or_module)
        if spec is None:
            raise ImportError(f"Could not load spec for {path_or_module}")

        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError(f"No loader for spec {spec}")

        spec.loader.exec_module(module)
    else:
        module = import_module(path_or_module)
    if object_path is None:
        obj = next((o for o in module.__dict__.values() if isinstance(o, config_type)), None)
        if obj is None:
            raise ValueError(f"Could not load {config_type.__name__} from {path_or_module}")
        return obj
    obj = getattr(module, object_path)
    assert isinstance(obj, config_type)
    return obj


def load_config(config_type: Type[T], config_path: str) -> T:
    if os.path.exists(config_path) and ".py" not in config_path:
        return config_type.load(config_path)

    return _load_config_from_python(config_type, config_path)
