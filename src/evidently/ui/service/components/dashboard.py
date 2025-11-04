from typing import Annotated
from typing import Dict

from litestar.di import Provide
from litestar.params import Dependency

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
        elif self.storage_type == "sql":
            from sqlalchemy import Engine

            from evidently.ui.service.storage.sql.dashboard import SQLDashboardManager

            def factory(engine: Annotated[Engine, Dependency()]):
                return SQLDashboardManager(engine)

            return factory
        raise ValueError("Unknown storage type {}".format(self.storage_type))

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {
            "dashboard_manager": Provide(self.provider()),
        }
