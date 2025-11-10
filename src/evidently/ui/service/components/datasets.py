from typing import ClassVar
from typing import Dict

from litestar.di import Provide

from evidently.ui.service.api.datasets import datasets_api
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.components.security import SecurityComponent
from evidently.ui.service.managers.datasets import DatasetManager
from evidently.ui.service.storage.local.dataset import DatasetFileStorage


class DatasetComponent(Component):
    """Component for dataset management."""

    __section__: ClassVar[str] = "datasets"

    def get_api_route_handlers(self, ctx: ComponentContext):
        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [datasets_api(guard)]

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        """Get dependencies for dataset components."""
        return {
            "dataset_manager": Provide(DatasetManager.provide, use_cache=True),
            "dataset_file_storage": Provide(DatasetFileStorage.provide, use_cache=True),
        }
