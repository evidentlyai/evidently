import json
import pathlib

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.ui.service.services.dashbord.base import DashboardManager
from evidently.ui.service.type_aliases import ProjectID


class JsonFileDashboardManager(DashboardManager):
    def __init__(self, path: str):
        self._path = path

    async def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        dashboard_path = pathlib.Path(self._path, str(project_id), "dashboard.json")
        if not dashboard_path.exists():
            return DashboardModel(tabs=[], panels=[])
        with open(dashboard_path) as dashboard:
            data = json.load(dashboard)
            return parse_obj_as(DashboardModel, data)

    async def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel) -> None:
        with open(pathlib.Path(self._path, str(project_id), "dashboard.json"), "w") as f_out:
            json.dump(dashboard.dict(), f_out, cls=NumpyEncoder)
