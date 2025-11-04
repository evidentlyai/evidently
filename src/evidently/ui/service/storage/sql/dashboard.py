import json
from typing import Optional

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.ui.service.services.dashbord.base import DashboardManager
from evidently.ui.service.type_aliases import ProjectID

from .base import BaseSQLStorage
from .models import ProjectSQLModel


class SQLDashboardManager(BaseSQLStorage, DashboardManager):
    """SQL-based dashboard manager implementation."""

    def __init__(self, engine):
        super().__init__(engine)

    @property
    def session(self) -> Session:
        """Get a session context manager."""
        return super().session

    async def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        """Get dashboard for a project."""
        with self.session as session:
            project: Optional[ProjectSQLModel] = session.scalar(
                select(ProjectSQLModel).where(ProjectSQLModel.id == project_id)
            )

            if project is None or project.dashboard_json is None:
                # Return default empty dashboard if not found
                return DashboardModel(tabs=[], panels=[])

            # Convert dashboard_json to DashboardModel
            from evidently._pydantic_compat import parse_obj_as

            return parse_obj_as(DashboardModel, project.dashboard_json)

    async def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel) -> None:
        """Save dashboard for a project."""
        with self.session as session:
            # Convert dashboard to JSON
            dashboard_json = json.loads(dashboard.json(cls=NumpyEncoder))

            # Update the dashboard_json field in the project table
            session.execute(
                update(ProjectSQLModel).where(ProjectSQLModel.id == project_id).values(dashboard_json=dashboard_json)
            )
            session.commit()
