import abc
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnMapping
from evidently.report import Report
from evidently.suite.base_suite import ReportBase
from evidently.suite.base_suite import Snapshot
from evidently.test_suite import TestSuite
from evidently.ui.base import Project
from evidently.ui.datasets import get_dataset_name_output_current
from evidently.ui.datasets import get_dataset_name_output_reference
from evidently.ui.type_aliases import STR_UUID
from evidently.ui.type_aliases import DatasetID
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import TeamID


class WorkspaceBase(abc.ABC):
    @abc.abstractmethod
    def create_project(self, name: str, description: Optional[str] = None, team_id: TeamID = None) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def add_project(self, project: Project, team_id: TeamID = None) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_project(self, project_id: STR_UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def list_projects(self, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None) -> List[Project]:
        raise NotImplementedError

    def _add_report_base(self, project_id: STR_UUID, report: ReportBase, include_data: bool = False):
        snapshot = report.to_snapshot()
        if include_data:
            run_from = "ws"
            current, reference = report.datasets()
            column_mapping = report.get_column_mapping()
            if current is not None:
                dataset_name_current = get_dataset_name_output_current(snapshot.is_report, snapshot.id, run_from)
                snapshot.links.datasets.output.current = self.add_dataset(
                    current, dataset_name_current, project_id, column_mapping=column_mapping
                )
            if reference is not None:
                dataset_name_reference = get_dataset_name_output_reference(snapshot.is_report, snapshot.id, run_from)
                snapshot.links.datasets.output.reference = self.add_dataset(
                    reference, dataset_name_reference, project_id, column_mapping=column_mapping
                )
        self.add_snapshot(project_id, snapshot)

    def add_report(self, project_id: STR_UUID, report: Report, include_data: bool = False):
        self._add_report_base(project_id, report, include_data)

    def add_test_suite(self, project_id: STR_UUID, test_suite: TestSuite, include_data: bool = False):
        self._add_report_base(project_id, test_suite, include_data)

    @abc.abstractmethod
    def add_snapshot(self, project_id: STR_UUID, snapshot: Snapshot):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def search_project(
        self, project_name: str, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None
    ) -> List[Project]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_dataset(
        self,
        data_or_path: Union[str, pd.DataFrame],
        name: str,
        project_id: STR_UUID,
        description: Optional[str] = None,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> DatasetID:
        raise NotImplementedError
