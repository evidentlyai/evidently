import datetime
import json
from typing import List
from typing import Optional
from typing import Union

from litestar.params import Dependency
from typing_extensions import Annotated

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.ui.base import BlobStorage
from evidently.legacy.ui.base import DataStorage
from evidently.legacy.ui.base import EntityType
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.base import ProjectMetadataStorage
from evidently.legacy.ui.base import SnapshotMetadata
from evidently.legacy.ui.errors import NotEnoughPermissions
from evidently.legacy.ui.errors import ProjectNotFound
from evidently.legacy.ui.managers.auth import AuthManager
from evidently.legacy.ui.managers.auth import DefaultRole
from evidently.legacy.ui.managers.auth import Permission
from evidently.legacy.ui.managers.base import BaseManager
from evidently.legacy.ui.type_aliases import ZERO_UUID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import UserID


class ProjectManager(BaseManager):
    project_metadata: ProjectMetadataStorage
    auth_manager: AuthManager
    blob_storage: BlobStorage
    data_storage: DataStorage

    def __init__(
        self,
        project_metadata: Annotated[ProjectMetadataStorage, Dependency()],
        auth_manager: Annotated[AuthManager, Dependency()],
        blob_storage: Annotated[BlobStorage, Dependency()],
        data_storage: Annotated[DataStorage, Dependency()],
        **dependencies,
    ):
        super().__init__(**dependencies)
        self.project_metadata: ProjectMetadataStorage = project_metadata
        self.auth_manager: AuthManager = auth_manager
        self.blob_storage = blob_storage
        self.data_storage = data_storage

    async def create_project(
        self,
        name: str,
        user_id: UserID,
        team_id: Optional[TeamID] = None,
        description: Optional[str] = None,
        org_id: Optional[TeamID] = None,
    ) -> Project:
        from evidently.legacy.ui.dashboards import DashboardConfig

        project = await self.add_project(
            Project(
                name=name,
                description=description,
                dashboard=DashboardConfig(name=name, panels=[]),
                team_id=team_id,
                org_id=org_id,
            ),
            user_id,
            team_id,
            org_id,
        )
        return project

    async def add_project(
        self, project: Project, user_id: UserID, team_id: Optional[TeamID] = None, org_id: Optional[OrgID] = None
    ) -> Project:
        user = await self.auth_manager.get_or_default_user(user_id)
        team = await self.auth_manager.get_team_or_error(team_id) if team_id else None
        if team:
            if not await self.auth_manager.check_entity_permission(
                user.id, EntityType.Team, team.id, Permission.TEAM_CREATE_PROJECT
            ):
                raise NotEnoughPermissions()
            project.team_id = team_id if team_id != ZERO_UUID else None
            org_id = team.org_id if team_id else None
            project.org_id = org_id
        elif org_id:
            project.org_id = org_id
            team = None
            if not await self.auth_manager.check_entity_permission(
                user.id, EntityType.Org, org_id, Permission.ORG_WRITE
            ):
                raise NotEnoughPermissions()

        project.created_at = project.created_at or datetime.datetime.now()
        project = (await self.project_metadata.add_project(project, user, team, org_id)).bind(self, user.id)
        await self.auth_manager.grant_entity_role(
            user.id,
            EntityType.Project,
            project.id,
            user.id,
            await self.auth_manager.get_default_role(DefaultRole.OWNER, EntityType.Project),
            skip_permission_check=True,
        )
        return project

    async def update_project(self, user_id: UserID, project: Project):
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project.id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        return await self.project_metadata.update_project(project)

    async def get_project(self, user_id: UserID, project_id: ProjectID) -> Optional[Project]:
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise ProjectNotFound()
        project = await self.project_metadata.get_project(project_id)
        if project is None:
            return None
        return project.bind(self, user.id)

    async def delete_project(self, user_id: UserID, project_id: ProjectID):
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_DELETE
        ):
            raise ProjectNotFound()
        return await self.project_metadata.delete_project(project_id)

    async def list_projects(self, user_id: UserID, team_id: Optional[TeamID], org_id: Optional[OrgID]) -> List[Project]:
        user = await self.auth_manager.get_or_default_user(user_id)
        project_ids = await self.auth_manager.get_available_project_ids(user.id, team_id, org_id)
        return [p.bind(self, user.id) for p in await self.project_metadata.list_projects(project_ids)]

    async def search_project(
        self,
        user_id: UserID,
        project_name: str,
        team_id: Optional[TeamID],
        org_id: Optional[OrgID],
    ) -> List[Project]:
        user = await self.auth_manager.get_or_default_user(user_id)
        project_ids = await self.auth_manager.get_available_project_ids(user.id, team_id, org_id)
        return [p.bind(self, user.id) for p in await self.project_metadata.search_project(project_name, project_ids)]

    async def add_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot: Snapshot):
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_SNAPSHOT_ADD
        ):
            raise ProjectNotFound()  # todo: better exception
        blob = await self.blob_storage.put_snapshot(project_id, snapshot)
        await self.project_metadata.add_snapshot(project_id, snapshot, blob)
        await self.data_storage.extract_points(project_id, snapshot)

    async def delete_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID):
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_SNAPSHOT_DELETE
        ):
            raise ProjectNotFound()  # todo: better exception
        # todo
        # self.data.remove_points(project_id, snapshot_id)
        # self.blob.delete_snapshot(project_id, snapshot_id)
        await self.project_metadata.delete_snapshot(project_id, snapshot_id)

    async def list_snapshots(
        self,
        user_id: UserID,
        project_id: ProjectID,
        include_reports: bool = True,
        include_test_suites: bool = True,
    ) -> List[SnapshotMetadata]:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        snapshots = await self.project_metadata.list_snapshots(project_id, include_reports, include_test_suites)
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
        with self.blob_storage.open_blob(snapshot.blob.id) as f:
            return parse_obj_as(Snapshot, json.load(f))

    async def get_snapshot_metadata(
        self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID
    ) -> SnapshotMetadata:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        meta = await self.project_metadata.get_snapshot_metadata(project_id, snapshot_id)
        meta.project.bind(self, user_id)
        return meta

    async def reload_snapshots(self, user_id: UserID, project_id: ProjectID):
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        await self.project_metadata.reload_snapshots(project_id)
