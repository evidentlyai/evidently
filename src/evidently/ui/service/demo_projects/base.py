import dataclasses
import warnings
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

from evidently import Dataset
from evidently.core.report import Snapshot
from evidently.ui.workspace import CloudWorkspace
from evidently.ui.workspace import Project
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase

DemoData = Tuple[Dataset, Dataset]


@dataclasses.dataclass
class DemoProject:
    name: str
    create_project: Callable[[WorkspaceBase, str], Project]
    create_data: Callable[[], DemoData]
    create_snapshot: Optional[Callable[[int, DemoData], Snapshot]]
    count: int

    def create(self, workspace: Union[str, WorkspaceBase]):
        if isinstance(workspace, WorkspaceBase):
            ws = workspace
        else:
            if workspace.startswith("http"):
                ws = CloudWorkspace(url=workspace)
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
                ws.add_run(project.id, snapshot)
