from typing import Literal

from .data_config import DataStorageConfig
from .data_config import MetadataStorageConfig


class InmemoryDataStorageConfig(DataStorageConfig):
    type: Literal["inmemory"] = "inmemory"
    path: str = "workspace"


class JsonFileMetadataStorageConfig(MetadataStorageConfig):
    type: Literal["json_file"] = "json_file"
    path: str = "workspace"
