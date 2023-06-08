import os
import uuid
from typing import Dict
from typing import List
from typing import Optional

from pydantic import UUID4
from pydantic import BaseModel
from pydantic import Field

from evidently.experimental.report_set import load_report_set
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report


class Project(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    path: str

    _reports: Optional[Dict[uuid.UUID, Report]] = None

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        if self._reports is None:
            self._reports = {r.id: r for r in load_report_set(self.path, cls=Report).values()}
        return self._reports


class Workspace:
    def __init__(self, path: str):
        self.path = path
        self._projects: Dict[uuid.UUID, Project] = self._load_projects()
        self._project_reports: Dict[uuid.UUID, List[Report]] = {}

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        # todo save/load projects metadata
        projects = [
            Project(name=p, path=os.path.join(self.path, p))
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())

    def list_project_reports(self, project_id: uuid.UUID) -> List[Report]:
        return list(self._projects[project_id].reports.values())

    def get_report_dashboard_info(self, project_id: uuid.UUID, report_id: uuid.UUID) -> DashboardInfo:
        _, dashboard_info, _ = self._projects[project_id].reports[report_id]._build_dashboard_info()
        return dashboard_info
