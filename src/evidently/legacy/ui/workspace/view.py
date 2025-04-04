import warnings
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
import uuid6

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.datasets import DatasetSourceType
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.type_aliases import STR_UUID
from evidently.legacy.ui.type_aliases import ZERO_UUID
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import UserID
from evidently.legacy.ui.workspace.base import WorkspaceBase
from evidently.legacy.utils.sync import async_to_sync


def _team_id_deprecation_message(team_id: Optional[TeamID]):
    if team_id is not None:
        warnings.warn(
            "The 'team_id' parameter is deprecated and will be removed in a future version. "
            "Please use 'org_id' instead.",
            DeprecationWarning,
            stacklevel=2,
        )


class WorkspaceView(WorkspaceBase):
    def __init__(
        self,
        user_id: Optional[UserID],
        project_manager: ProjectManager,
    ):
        self.project_manager = project_manager
        self.user_id = user_id or ZERO_UUID

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        team_id: Optional[TeamID] = None,
        org_id: Optional[OrgID] = None,
    ) -> Project:
        _team_id_deprecation_message(team_id)
        return async_to_sync(
            self.project_manager.create_project(
                name, user_id=self.user_id, team_id=team_id, description=description, org_id=org_id
            )
        )

    def add_project(
        self, project: Project, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None
    ) -> Project:
        _team_id_deprecation_message(team_id)
        project = async_to_sync(
            self.project_manager.add_project(project, user_id=self.user_id, team_id=team_id, org_id=org_id)
        )
        return project

    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        if isinstance(project_id, str):
            project_id = uuid6.UUID(project_id)
        return async_to_sync(self.project_manager.get_project(self.user_id, project_id))

    def delete_project(self, project_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid6.UUID(project_id)
        async_to_sync(self.project_manager.delete_project(self.user_id, project_id))

    def list_projects(self, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None) -> List[Project]:
        _team_id_deprecation_message(team_id)
        return async_to_sync(
            self.project_manager.list_projects(self.user_id, team_id or ZERO_UUID, org_id or ZERO_UUID)
        )

    def add_snapshot(self, project_id: STR_UUID, snapshot: Snapshot):
        if isinstance(project_id, str):
            project_id = uuid6.UUID(project_id)
        async_to_sync(self.project_manager.add_snapshot(self.user_id, project_id, snapshot))

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid6.UUID(project_id)
        if isinstance(snapshot_id, str):
            snapshot_id = uuid6.UUID(snapshot_id)
        async_to_sync(self.project_manager.delete_snapshot(self.user_id, project_id, snapshot_id))

    def search_project(
        self, project_name: str, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None
    ) -> List[Project]:
        _team_id_deprecation_message(team_id)
        return async_to_sync(
            self.project_manager.search_project(self.user_id, project_name, team_id or ZERO_UUID, org_id or ZERO_UUID)
        )

    def add_dataset(
        self,
        data_or_path: Union[str, pd.DataFrame],
        name: str,
        project_id: STR_UUID,
        description: Optional[str] = None,
        column_mapping: Optional[ColumnMapping] = None,
        dataset_source: DatasetSourceType = DatasetSourceType.file,
    ) -> DatasetID:
        raise NotImplementedError("Adding datasets is not supported yet")


class LocalWorkspaceView(WorkspaceView):
    def __init__(self, path: str):
        from evidently.legacy.ui.storage.local import create_local_project_manager

        self.path = path
        super().__init__(None, create_local_project_manager(path=path, autorefresh=False))

    @classmethod
    def create(cls, path: str):
        return LocalWorkspaceView(path)

    def refresh(self):
        from evidently.legacy.ui.storage.local import create_local_project_manager

        self.project_manager = create_local_project_manager(path=self.path, autorefresh=False)


Workspace = LocalWorkspaceView
