import abc

from evidently.sdk.models import DashboardModel
from evidently.ui.service.type_aliases import ProjectID


class DashboardManager:
    @abc.abstractmethod
    async def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel) -> None:
        raise NotImplementedError
