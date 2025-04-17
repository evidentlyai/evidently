import json
import posixpath
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from litestar.exceptions import HTTPException
from litestar.params import Dependency
from typing_extensions import Annotated

from evidently._pydantic_compat import parse_obj_as
from evidently.core.serialization import SnapshotModel
from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import EntityType
from evidently.ui.service.base import Project
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.base import SeriesFilter
from evidently.ui.service.base import SeriesResponse
from evidently.ui.service.errors import NotEnoughPermissions
from evidently.ui.service.errors import ProjectNotFound
from evidently.ui.service.managers.auth import AuthManager
from evidently.ui.service.managers.auth import DefaultRole
from evidently.ui.service.managers.auth import Permission
from evidently.ui.service.managers.base import BaseManager
from evidently.ui.service.services.dashbord.base import DashboardManager
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID
from evidently.ui.service.type_aliases import TeamID
from evidently.ui.service.type_aliases import UserID

SNAPSHOTS = "snapshots"


class ProjectManager(BaseManager):
    project_metadata: ProjectMetadataStorage
    dashboard_manager: DashboardManager
    auth_manager: AuthManager
    blob_storage: BlobStorage
    data_storage: DataStorage

    def __init__(
        self,
        project_metadata: Annotated[ProjectMetadataStorage, Dependency()],
        auth_manager: Annotated[AuthManager, Dependency()],
        blob_storage: Annotated[BlobStorage, Dependency()],
        data_storage: Annotated[DataStorage, Dependency()],
        dashboard_manager: Annotated[DashboardManager, Dependency()],
        **dependencies,
    ):
        super().__init__(**dependencies)
        self.project_metadata: ProjectMetadataStorage = project_metadata
        self.auth_manager: AuthManager = auth_manager
        self.blob_storage = blob_storage
        self.data_storage = data_storage
        self.dashboard_manager = dashboard_manager

    async def create_project(
        self,
        name: str,
        user_id: UserID,
        team_id: Optional[TeamID] = None,
        description: Optional[str] = None,
        org_id: Optional[TeamID] = None,
    ) -> Project:
        project = await self.add_project(
            Project(
                name=name,
                description=description,
                team_id=team_id,
                org_id=org_id,
            ),
            user_id,
            org_id,
        )
        return project

    async def add_project(self, project: Project, user_id: UserID, org_id: Optional[OrgID] = None) -> Project:
        user = await self.auth_manager.get_or_default_user(user_id)
        if org_id:
            project.org_id = org_id
            if not await self.auth_manager.check_entity_permission(
                user.id, EntityType.Org, org_id, Permission.ORG_WRITE
            ):
                raise NotEnoughPermissions()

        project.created_at = project.created_at or datetime.now()
        project = (await self.project_metadata.add_project(project, user, org_id)).bind(self, user.id)
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

    async def add_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot: SnapshotModel) -> SnapshotID:
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id, EntityType.Project, project_id, Permission.PROJECT_SNAPSHOT_ADD
        ):
            raise NotEnoughPermissions()
        snapshot_id = await self.project_metadata.add_snapshot(project_id, snapshot)
        blob_id = self._create_path_for_snapshot(project_id, snapshot_id)
        await self.blob_storage.put_blob(blob_id, json.dumps(snapshot.dict(), cls=NumpyEncoder))
        await self.data_storage.add_snapshot_points(project_id, snapshot_id, snapshot)
        return snapshot_id

    async def delete_snapshot(self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID):
        user = await self.auth_manager.get_or_default_user(user_id)
        if not await self.auth_manager.check_entity_permission(
            user.id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        await self.auth_manager.validate_permission(
            user.id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_SNAPSHOT_DELETE,
        )
        # TODO: Support points for dashboard.
        await self.project_metadata.delete_snapshot(project_id, snapshot_id)

    async def list_snapshots(
        self,
        user_id: UserID,
        project_id: ProjectID,
    ) -> List[SnapshotMetadataModel]:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        snapshots = await self.project_metadata.list_snapshots(project_id)
        return snapshots

    async def load_snapshot(
        self,
        user_id: UserID,
        project_id: ProjectID,
        snapshot: SnapshotID,
    ) -> SnapshotModel:
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        with self.blob_storage.open_blob(self._create_path_for_snapshot(project_id, snapshot)) as f:
            return parse_obj_as(SnapshotModel, json.load(f))

    async def get_snapshot_metadata(
        self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID
    ) -> SnapshotMetadataModel:
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise NotEnoughPermissions()
        meta = await self.project_metadata.get_snapshot_metadata(project_id, snapshot_id)
        return meta

    async def reload_snapshots(self, user_id: UserID, project_id: ProjectID):
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        await self.project_metadata.reload_snapshots(project_id)

    def _create_path_for_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        return posixpath.join(str(project_id), SNAPSHOTS, str(snapshot_id)) + ".json"

    async def get_project_dashboard(self, user_id: UserID, project_id: ProjectID) -> DashboardModel:
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        return await self.dashboard_manager.get_dashboard(project_id)

    async def save_project_dashboard(self, user_id: UserID, project_id: ProjectID, dashboard: DashboardModel):
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_WRITE,
        ):
            raise NotEnoughPermissions()
        if len(dashboard.tabs) > 1:
            raise HTTPException(status_code=400, detail="Multiple tabs are not supported in Evidently OSS")
        await self.dashboard_manager.save_dashboard(project_id, dashboard)

    async def get_metrics(
        self,
        user_id: UserID,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
    ):
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        return await self.data_storage.get_metrics(project_id, tags, metadata)

    async def get_metric_labels(
        self,
        user_id: UserID,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
    ):
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        return await self.data_storage.get_metric_labels(project_id, tags, metadata, metric)

    async def get_metric_label_values(
        self,
        user_id: UserID,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
        label: str,
    ):
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        return await self.data_storage.get_metric_label_values(project_id, tags, metadata, metric, label)

    async def get_data_series(
        self,
        user_id: UserID,
        project_id: ProjectID,
        series_filter: List[SeriesFilter],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
    ) -> SeriesResponse:
        if not await self.auth_manager.check_entity_permission(
            user_id,
            EntityType.Project,
            project_id,
            Permission.PROJECT_READ,
        ):
            raise ProjectNotFound()
        return await self.data_storage.get_data_series(project_id, series_filter, start_time, end_time)
