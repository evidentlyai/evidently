from fsspec.implementations.local import LocalFileSystem

from ...managers.auth import AuthManager
from ...managers.projects import ProjectManager
from ...services.dashbord.file import JsonFileDashboardManager
from ..common import NoopAuthManager
from .base import FSSpecBlobStorage
from .base import InMemoryDataStorage
from .base import JsonFileProjectMetadataStorage
from .base import LocalState


def start_workspace_watchdog(path: str, state: LocalState):
    from watchdog.observers import Observer

    from evidently.ui.service.storage.local.watcher import WorkspaceDirHandler

    observer = Observer()
    observer.schedule(WorkspaceDirHandler(state), path, recursive=True)
    observer.start()
    print(f"Observer for '{path}' started")


def create_local_project_manager(path: str, autorefresh: bool, auth: AuthManager = None) -> ProjectManager:
    state = LocalState.load(path, None)

    metadata = JsonFileProjectMetadataStorage(path=path, local_state=state)
    data = InMemoryDataStorage(path=path, local_state=state)
    project_manager = ProjectManager(
        project_metadata=metadata,
        blob_storage=FSSpecBlobStorage(base_path=path),
        data_storage=data,
        auth_manager=auth or NoopAuthManager(),
        dashboard_manager=JsonFileDashboardManager(path=path, local_state=state),
    )
    state.project_manager = project_manager

    fs = state.location.fs
    if autorefresh and isinstance(fs, LocalFileSystem):
        start_workspace_watchdog(path, state)
    return project_manager
