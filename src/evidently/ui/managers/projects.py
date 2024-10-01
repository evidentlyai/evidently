import datetime
import json
from typing import Annotated
from typing import List
from typing import Optional
from typing import Union

from litestar.params import Dependency

from evidently._pydantic_compat import parse_obj_as
from evidently.suite.base_suite import Snapshot
from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import EntityType
from evidently.ui.base import MetadataStorage
from evidently.ui.base import Project
from evidently.ui.base import SnapshotMetadata
from evidently.ui.errors import NotEnoughPermissions
from evidently.ui.errors import ProjectNotFound
from evidently.ui.managers.auth import AuthManager
from evidently.ui.managers.auth import DefaultRole
from evidently.ui.managers.auth import Permission
from evidently.ui.managers.base import BaseManager
from evidently.ui.type_aliases import ZERO_UUID
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import SnapshotID
from evidently.ui.type_aliases import TeamID
from evidently.ui.type_aliases import UserID


class ProjectManager(BaseManager):
    def __init__(
        self,
        metadata: Annotated[MetadataStorage, Dependency()],
        auth: Annotated[AuthManager, Dependency()],
        blob: Annotated[BlobStorage, Dependency()],
        data: Annotated[DataStorage, Dependency()],
    ):
        self.metadata: MetadataStorage = metadata
        self.auth: AuthManager = auth
        self.blob = blob
        self.data = data

    async def create_project(
        self,
        name: str,
        user_id: UserID,
        team_id: TeamID,
        description: Optional[str] = None,
    ) -> Project:
        from evidently.ui.dashboards import DashboardConfig

        project = await self.add_project(
            Project(
                name=name,
                description=description,
                dashboard=DashboardConfig(name=name, panels=[]),
                team_id=team_id,
            ),
            user_id,
            team_id,
        )
        return project

    async def add_project(self, project: Project, user_id: UserID, team_id: TeamID) -> Project:
        user = await self.auth.get_or_default_user(user_id)
        team = await self.auth.get_team_or_error(team_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Team, team.id, Permission.TEAM_CREATE_PROJECT
        ):
            raise NotEnoughPermissions()
        project.team_id = team_id if team_id != ZERO_UUID else None
        project.created_at = project.created_at or datetime.datetime.now()
        project = (await self.metadata.add_project(project, user, team)).bind(self, user.id)
        await self.auth.grant_entity_role(
            user.id,
            EntityType.Project,
            project.id,
            user.id,
            await self.auth.get_default_role(DefaultRole.OWNER, EntityType.Project),
            skip_permission_check=True,
        )
        return project

    async def update_project(self, user_id: UserID, project: Project):
        user = await self.auth.get_or_default_user(user_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Project, project.id, Permission.PROJECT_WRITE
        ):
            raise ProjectNotFound()
        return await self.metadata.update_project(project)

    async def get_project(self, user_id: UserID, project_id: ProjectID) -> Optional[Project]:
        user = await self.auth.get_or_default_user(user_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise ProjectNotFound()
        project = await self.metadata.get_project(project_id)
        if project is None:
            return None
        return project.bind(self, user.id)

    async def delete_project(self, user_id: UserID, project_id: ProjectID):
        user = await self.auth.get_or_default_user(user_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_DELETE
        ):
            raise ProjectNotFound()
        return await self.metadata.delete_project(project_id)

    async def list_projects(self, user_id: UserID, team_id: Optional[TeamID], org_id: Optional[OrgID]) -> List[Project]:
        user = await self.auth.get_or_default_user(user_id)
        project_ids = await self.auth.get_available_project_ids(user.id, team_id, org_id)
        return [p.bind(self, user.id) for p in await self.metadata.list_projects(project_ids)]

    async def search_project(
        self,
        user_id: UserID,
        project_name: str,
        team_id: Optional[TeamID],
        org_id: Optional[OrgID],
    ) -> List[Project]:
        user = await self.auth.get_or_default_user(user_id)
        project_ids = await self.auth.get_available_project_ids(user.id, team_id, org_id)
        return [p.bind(self, user.id) for p in await self.metadata.search_project(project_name, project_ids)]

    async def add_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot: Snapshot):
        user = await self.auth.get_or_default_user(user_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_SNAPSHOT_ADD
        ):
            raise ProjectNotFound()  # todo: better exception
        blob = await self.blob.put_snapshot(project_id, snapshot)
        await self.metadata.add_snapshot(project_id, snapshot, blob)
        await self.data.extract_points(project_id, snapshot)

    async def delete_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID):
        user = await self.auth.get_or_default_user(user_id)
        if not await self.auth.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_SNAPSHOT_DELETE
        ):
            raise ProjectNotFound()  # todo: better exception
        # todo
        # self.data.remove_points(project_id, snapshot_id)
        # self.blob.delete_snapshot(project_id, snapshot_id)
        await self.metadata.delete_snapshot(project_id, snapshot_id)

    async def list_snapshots(
        self,
        user_id: UserID,
        project_id: ProjectID,
        include_reports: bool = True,
        include_test_suites: bool = True,
    ) -> List[SnapshotMetadata]:
        if not await self.auth.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        snapshots = await self.metadata.list_snapshots(project_id, include_reports, include_test_suites)
        for s in snapshots:
            s.project.bind(self, user_id)
        return snapshots

    async def load_snapshot(
        self,
        user_id: UserID,
        project_id: ProjectID,
        snapshot: Union[SnapshotID, SnapshotMetadata],
    ) -> Snapshot:
        if isinstance(snapshot, SnapshotID):
            snapshot = await self.get_snapshot_metadata(user_id, project_id, snapshot)
        with self.blob.open_blob(snapshot.blob.id) as f:
            return parse_obj_as(Snapshot, json.load(f))

    async def get_snapshot_metadata(
        self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID
    ) -> SnapshotMetadata:
        if not await self.auth.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        meta = await self.metadata.get_snapshot_metadata(project_id, snapshot_id)
        meta.project.bind(self, user_id)
        return meta

    async def reload_snapshots(self, user_id: UserID, project_id: ProjectID):
        if not await self.auth.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        await self.metadata.reload_snapshots(project_id)
