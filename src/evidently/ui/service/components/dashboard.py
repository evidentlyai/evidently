from typing import Dict

from litestar.di import Provide

from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.services.dashbord.file import JsonFileDashboardManager


class DashboardComponent(Component):
    __service_name__ = "dashboards"
    storage_type = "file"
    path: str = "workspace"

    def provider(self):
        if self.storage_type == "file":

            async def factory():
                return JsonFileDashboardManager(self.path)

            return factory
        raise ValueError("Unknown storage type {}".format(self.storage_type))

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {
            "dashboard_manager": Provide(self.provider()),
        }
