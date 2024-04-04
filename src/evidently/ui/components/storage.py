from abc import ABC
from typing import Callable
from typing import Dict

from litestar.di import Provide

from evidently.ui.base import ProjectManager
from evidently.ui.components.base import Component
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.storage.local import create_local_project_manager


class StorageComponent(Component, ABC):
    def project_manager_factory(self) -> Callable[[], ProjectManager]:
        raise NotImplementedError

    def get_dependencies(self) -> Dict[str, Provide]:
        return {
            "project_manager": Provide(
                self.project_manager_factory(),
                sync_to_thread=True,
                use_cache=True,
            )
        }


class LocalStorageComponent(StorageComponent):
    path: str = "workspace"
    autorefresh: bool = True

    def project_manager_factory(self) -> Callable[[], ProjectManager]:
        return lambda: create_local_project_manager(self.path, autorefresh=self.autorefresh, auth=NoopAuthManager())
