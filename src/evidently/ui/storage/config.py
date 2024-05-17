import pydantic

from .data_config import FSSpecBlobStorageConfig
from .local_data_config import InmemoryDataStorageConfig
from .local_data_config import JsonFileMetadataStorageConfig


class StorageConfig(pydantic.BaseModel):
    metadata: "JsonFileMetadataStorageConfig" = JsonFileMetadataStorageConfig()
    data: InmemoryDataStorageConfig = InmemoryDataStorageConfig()
    blob: FSSpecBlobStorageConfig = FSSpecBlobStorageConfig()
