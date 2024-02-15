from .config import StorageConfig


class LocalStorageConfig(StorageConfig):
    path: str = "workspace"
    autoupdate: bool = False
