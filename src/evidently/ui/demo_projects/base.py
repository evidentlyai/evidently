import dataclasses
import warnings
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.suite.base_suite import Snapshot
from evidently.test_suite import TestSuite
from evidently.ui.base import Project
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
from evidently.ui.workspace.remote import RemoteWorkspace

DemoData = Tuple[pd.DataFrame, pd.DataFrame, ColumnMapping]


@dataclasses.dataclass
class DemoProject:
    name: str

    create_project: Callable[[WorkspaceBase, str], Project]

    create_data: Callable[[], DemoData]
    create_report: Optional[Callable[[int, DemoData], Report]]
    create_snapshot: Optional[Callable[[int, DemoData], Snapshot]]
    create_test_suite: Optional[Callable[[int, DemoData], TestSuite]]
    count: int

    def create(self, workspace: Union[str, WorkspaceBase]):
        if isinstance(workspace, WorkspaceBase):
            ws = workspace
        else:
            if workspace.startswith("http"):
                ws = RemoteWorkspace(workspace)
            else:
                ws = Workspace.create(workspace)

        # todo: fix all the warnings
        warnings.filterwarnings("ignore")
        warnings.simplefilter("ignore")

        project = self.create_project(ws, self.name)
        data = self.create_data()

        for i in range(0, self.count):
            if self.create_snapshot is not None:
                snapshot = self.create_snapshot(i, data)
                ws.add_snapshot(project.id, snapshot)

            if self.create_report is not None:
                report = self.create_report(i, data)
                ws.add_report(project.id, report)

            if self.create_test_suite is not None:
                test_suite = self.create_test_suite(i, data)
                ws.add_test_suite(project.id, test_suite)
