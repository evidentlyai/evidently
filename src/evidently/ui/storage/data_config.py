import pydantic


class MetadataStorageConfig(pydantic.BaseModel):
    type: str


class DataStorageConfig(pydantic.BaseModel):
    type: str


class FSSpecBlobStorageConfig(pydantic.BaseModel):
    path: str = "workspace"
