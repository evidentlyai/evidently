from fsspec.implementations.local import LocalFileSystem

from evidently.ui.base import ProjectManager
from evidently.ui.config import StorageConfig

from ..common import NoopAuthManager
from .base import FSSpecBlobStorage
from .base import InMemoryDataStorage
from .base import JsonFileMetadataStorage
from .base import LocalState


class LocalStorageConfig(StorageConfig):
    path: str = "workspace"
    autorefresh: bool = False

    def create_project_manager(self) -> ProjectManager:
        metadata = JsonFileMetadataStorage(path=self.path)
        data = InMemoryDataStorage(path=self.path)
        project_manager = ProjectManager(
            metadata=metadata, blob=FSSpecBlobStorage(base_path=self.path), data=data, auth=NoopAuthManager()
        )
        state = LocalState.load(self.path, project_manager)
        project_manager.data._state = project_manager.metadata._state = state

        fs = state.location.fs
        if self.autorefresh and isinstance(fs, LocalFileSystem):
            from watchdog.observers import Observer

            from evidently.ui.storage.local.watcher import WorkspaceDirHandler

            observer = Observer()
            observer.schedule(WorkspaceDirHandler(state), self.path, recursive=True)
            observer.start()
            print(f"Observer for '{self.path}' started")
        return project_manager
