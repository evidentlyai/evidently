import os
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import UUID4
from pydantic import BaseModel
from pydantic import Field

from evidently.experimental.report_set import load_report_set
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite


class Project(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    path: str

    _reports: Optional[Dict[uuid.UUID, Report]] = None
    _test_suites: Optional[Dict[uuid.UUID, TestSuite]] = None

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        if self._reports is None:
            self._reports = {r.id: r for r in load_report_set(os.path.join(self.path, "reports"), cls=Report).values()}
        return self._reports

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        if self._test_suites is None:
            self._test_suites = {r.id: r for r in load_report_set(os.path.join(self.path, "test_suites"), cls=TestSuite).values()}
        return self._test_suites

    def get_item(self, report_id: uuid.UUID) -> Optional[Union[Report, TestSuite]]:
        return self.reports.get(report_id) or self.test_suites.get(report_id)


class Workspace:
    def __init__(self, path: str):
        self.path = path
        self._projects: Dict[uuid.UUID, Project] = self._load_projects()

    def _load_projects(self) -> Dict[uuid.UUID, Project]:
        # todo save/load projects metadata
        projects = [
            Project(name=p, path=os.path.join(self.path, p))
            for p in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, p))
        ]
        return {p.id: p for p in projects}

    def get_project(self, project_id: uuid.UUID) -> Project:
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[Project]:
        return list(self._projects.values())
