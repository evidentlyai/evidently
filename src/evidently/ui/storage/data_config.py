from evidently._pydantic_compat import BaseModel


class MetadataStorageConfig(BaseModel):
    type: str


class DataStorageConfig(BaseModel):
    type: str


class FSSpecBlobStorageConfig(BaseModel):
    path: str = "workspace"
