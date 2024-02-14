import contextlib
import datetime
import json
import uuid
from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union
from uuid import UUID

from evidently._pydantic_compat import UUID4
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import parse_obj_as
from evidently.model.dashboard import DashboardInfo
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.renderers.notebook_utils import determine_template
from evidently.suite.base_suite import MetadataValueType
from evidently.suite.base_suite import ReportBase
from evidently.suite.base_suite import Snapshot
from evidently.ui.dashboards.base import DashboardConfig
from evidently.ui.dashboards.base import PanelValue
from evidently.ui.dashboards.base import ReportFilter
from evidently.ui.dashboards.test_suites import TestFilter
from evidently.ui.errors import NotEnoughPermissions
from evidently.ui.errors import ProjectNotFound
from evidently.ui.errors import TeamNotFound
from evidently.ui.type_aliases import BlobID
from evidently.ui.type_aliases import DataPoints
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import RoleID
from evidently.ui.type_aliases import SnapshotID
from evidently.ui.type_aliases import TeamID
from evidently.ui.type_aliases import TestResultPoints
from evidently.ui.type_aliases import UserID
from evidently.utils import NumpyEncoder
from evidently.utils.dashboard import TemplateParams


class SnapshotMetadata(BaseModel):
    id: UUID4
    name: Optional[str] = None
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    is_report: bool
    blob_id: BlobID

    _project: "Project" = PrivateAttr(None)
    _dashboard_info: "DashboardInfo" = PrivateAttr(None)
    _additional_graphs: Dict[str, dict] = PrivateAttr(None)

    @property
    def project(self):
        return self._project

    def load(self) -> Snapshot:
        return self.project.project_manager.load_snapshot(self.project._user_id, self.project.id, self.id)

    def as_report_base(self) -> ReportBase:
        value = self.load()
        return value.as_report() if value.is_report else value.as_test_suite()

    def bind(self, project: "Project"):
        self._project = project
        return self

    @classmethod
    def from_snapshot(cls, snapshot: Snapshot, blob_id: BlobID) -> "SnapshotMetadata":
        return SnapshotMetadata(
            id=snapshot.id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            is_report=snapshot.is_report,
            blob_id=blob_id,
        )

    @property
    def dashboard_info(self):
        if self._dashboard_info is None:
            _, self._dashboard_info, self._additional_graphs = self.as_report_base()._build_dashboard_info()
        return self._dashboard_info

    @property
    def additional_graphs(self):
        if self._additional_graphs is None:
            _, self._dashboard_info, self._additional_graphs = self.as_report_base()._build_dashboard_info()
        return self._additional_graphs


class Org(BaseModel):
    id: OrgID = Field(default_factory=uuid.uuid4)
    name: str


class Team(BaseModel):
    id: TeamID = Field(default_factory=uuid.uuid4)
    name: str


class User(BaseModel):
    id: UserID = Field(default_factory=uuid.uuid4)
    name: str


def _default_dashboard():
    from evidently.ui.dashboards import DashboardConfig

    return DashboardConfig(name="", panels=[])


class Project(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    id: ProjectID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None
    dashboard: "DashboardConfig" = Field(default_factory=_default_dashboard)

    team_id: Optional[TeamID]

    date_from: Optional[datetime.datetime] = None
    date_to: Optional[datetime.datetime] = None

    _project_manager: "ProjectManager" = PrivateAttr(None)
    _user_id: UserID = PrivateAttr(None)

    def bind(self, project_manager: Optional["ProjectManager"], user_id: Optional[UserID]):
        # todo: better typing (add optional or forbid optional)
        self._project_manager = project_manager  # type: ignore[assignment]
        self._user_id = user_id  # type: ignore[assignment]
        return self

    @property
    def project_manager(self) -> "ProjectManager":
        if self._project_manager is None:
            raise ValueError("Project is not binded")
        return self._project_manager

    def save(self):
        self.project_manager.update_project(self._user_id, self)
        return self

    def load_snapshot(self, snapshot_id: uuid.UUID) -> Snapshot:
        return self.project_manager.load_snapshot(self._user_id, self.id, snapshot_id)

    def add_snapshot(self, snapshot: Snapshot):
        self.project_manager.add_snapshot(self._user_id, self.id, snapshot)

    def delete_snapshot(self, snapshot_id: Union[str, uuid.UUID]):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid.UUID(snapshot_id)
        self.project_manager.delete_snapshot(self._user_id, self.id, snapshot_id)

    def list_snapshots(self, include_reports: bool = True, include_test_suites: bool = True) -> List[SnapshotMetadata]:
        return self.project_manager.list_snapshots(self._user_id, self.id, include_reports, include_test_suites)

    def get_snapshot_metadata(self, id: uuid.UUID) -> SnapshotMetadata:
        return self.project_manager.get_snapshot_metadata(self._user_id, self.id, id)

    def build_dashboard_info(
        self, timestamp_start: Optional[datetime.datetime], timestamp_end: Optional[datetime.datetime]
    ) -> DashboardInfo:
        return self.dashboard.build(self.project_manager.data, self.id, timestamp_start, timestamp_end)

    def show_dashboard(
        self, timestamp_start: Optional[datetime.datetime] = None, timestamp_end: Optional[datetime.datetime] = None
    ):
        dashboard_info = self.build_dashboard_info(timestamp_start, timestamp_end)
        template_params = TemplateParams(
            dashboard_id="pd_" + str(uuid.uuid4()).replace("-", ""),
            dashboard_info=dashboard_info,
            additional_graphs={},
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(determine_template("inline")(params=template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def reload(self, reload_snapshots: bool = False):
        # fixme: reload snapshots
        project = self.project_manager.get_project(self._user_id, self.id)
        self.__dict__.update(project.__dict__)

        if reload_snapshots:
            self.project_manager.reload_snapshots(self._user_id, self.id)


class MetadataStorage(EvidentlyBaseModel, ABC):
    @abstractmethod
    def add_project(self, project: Project, user: User, team: Team, org: Org) -> Project:
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: ProjectID) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: ProjectID):
        raise NotImplementedError

    @abstractmethod
    def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot, blob_id: str):
        raise NotImplementedError

    @abstractmethod
    def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        raise NotImplementedError

    @abstractmethod
    def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def list_snapshots(
        self, project_id: ProjectID, include_reports: bool = True, include_test_suites: bool = True
    ) -> List[SnapshotMetadata]:
        raise NotImplementedError

    @abstractmethod
    def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadata:
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def reload_snapshots(self, project_id: ProjectID):
        raise NotImplementedError


class BlobStorage(EvidentlyBaseModel, ABC):
    @abstractmethod
    @contextlib.contextmanager
    def open_blob(self, id: BlobID):
        raise NotImplementedError

    def put_blob(self, path: str, obj):
        raise NotImplementedError

    def get_snapshot_blob_id(self, project_id: UUID, snapshot: Snapshot) -> BlobID:
        raise NotImplementedError

    def put_snapshot(self, project_id: UUID, snapshot: Snapshot) -> BlobID:
        id = self.get_snapshot_blob_id(project_id, snapshot)
        self.put_blob(id, json.dumps(snapshot.dict(), cls=NumpyEncoder))
        return id


class DataStorage(EvidentlyBaseModel, ABC):
    @abstractmethod
    def extract_points(self, project_id: ProjectID, snapshot: Snapshot):
        raise NotImplementedError

    @abstractmethod
    def load_points(
        self,
        project_id: ProjectID,
        filter: "ReportFilter",
        values: List["PanelValue"],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DataPoints:
        raise NotImplementedError

    @abstractmethod
    def load_test_results(
        self,
        project_id: ProjectID,
        filter: "ReportFilter",
        test_filters: List["TestFilter"],
        time_agg: Optional[str],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> TestResultPoints:
        raise NotImplementedError


class Permission(Enum):
    GRANT_ROLE = "all_grant_role"
    REVOKE_ROLE = "all_revoke_role"

    # ORG_USER_REMOVE_SELF = "org_user_remove_self"

    TEAM_READ = "team_read"
    TEAM_WRITE = "team_write"
    TEAM_DELETE = "team_delete"
    # TEAM_USER_ADD = "team_user_add"
    # TEAM_USER_REMOVE = "team_user_remove"
    # TEAM_USER_REMOVE_SELF = "team_user_remove_self"

    PROJECT_READ = "project_read"
    PROJECT_WRITE = "project_write"
    PROJECT_DELETE = "project_delete"
    PROJECT_SNAPSHOT_ADD = "project_snapshot_add"
    PROJECT_SNAPSHOT_DELETE = "project_snapshot_delete"


class EntityType(Enum):
    Project = "project"
    Team = "team"
    Org = "org"


class Role(BaseModel):
    id: RoleID
    name: str


class DefaultRole(Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


DEFAULT_ROLE_PERMISSIONS: Dict[DefaultRole, Set[Permission]] = {
    DefaultRole.OWNER: set(Permission),
    DefaultRole.EDITOR: {
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.PROJECT_SNAPSHOT_ADD,
    },
    DefaultRole.VIEWER: {Permission.TEAM_READ, Permission.PROJECT_READ},
}


class AuthManager(EvidentlyBaseModel):
    allow_default_user: bool = True

    @abstractmethod
    def get_available_project_ids(self, user_id: UserID, org_id: OrgID) -> Optional[Set[ProjectID]]:
        raise NotImplementedError

    # @abstractmethod
    # def check_team1_permission(self, user_id: UserID, team_id: TeamID, permission: Permission) -> bool:
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def check_projec1t_permission(self, user_id: UserID, project_id: ProjectID, permission: Permission) -> bool:
    #     raise NotImplementedError

    @abstractmethod
    def check_entity_permission(
        self, user_id: UserID, entity_id: uuid.UUID, entity_type: EntityType, permission: Permission
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user_id: UserID, name: Optional[str]) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id: UserID) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_default_user(self) -> User:
        raise NotImplementedError

    def get_or_create_user(self, user_id: UserID) -> User:
        user = self.get_user(user_id)
        if user is None:
            user = self.create_user(user_id, str(user_id))
        return user

    @abstractmethod
    def create_team(self, author: UserID, team: Team, org_id: OrgID) -> Team:
        raise NotImplementedError

    @abstractmethod
    def get_team(self, team_id: TeamID) -> Optional[Team]:
        raise NotImplementedError

    # @abstractmethod
    # def get_default_team(self, user_id: UserID) -> Team:
    #     raise NotImplementedError

    @abstractmethod
    def create_org(self, owner: UserID, org: Org):
        raise NotImplementedError

    @abstractmethod
    def get_org(self, org_id: OrgID) -> Optional[Org]:
        raise NotImplementedError

    def get_or_create_team(self, team_id: TeamID, author: UserID, name: str, org_id: Optional[OrgID]):
        team = self.get_team(team_id)
        if team is None:
            team = self.create_team(author, Team(name=name), org_id)
        return team

    def get_or_default_user(self, user_id: Optional[UserID]) -> User:
        return self.get_or_create_user(user_id) if user_id is not None else self.get_default_user()

    # def get_or_default_team(self, team_id: Optional[TeamID], user_id: UserID) -> Team:
    #     if team_id is None:
    #         return self.get_default_team(user_id)
    #     team = self.get_team(team_id)
    #     if team is None:
    #         raise TeamNotFound()
    #
    #     return team

    # @abstractmethod
    # def _list_user_teams(self, user_id: UserID, include_virtual: bool) -> List[Team]:
    #     raise NotImplementedError
    #
    # def list_user_teams(self, user_id: Optional[UserID], include_virtual: bool) -> List[Team]:
    #     if user_id is None:
    #         user_id = self.get_default_user().id
    #     return self._list_user_teams(user_id, include_virtual)

    @abstractmethod
    def _delete_team(self, team_id: TeamID):
        raise NotImplementedError

    def delete_team(self, user_id: UserID, team_id: TeamID):
        if not self.check_entity_permission(user_id, team_id, EntityType.Team, Permission.TEAM_DELETE):
            raise NotEnoughPermissions()
        self._delete_team(team_id)

    @abstractmethod
    def _list_team_users(self, team_id: TeamID) -> List[User]:
        raise NotImplementedError

    def list_team_users(self, user_id: UserID, team_id: TeamID) -> List[User]:
        if not self.check_entity_permission(user_id, team_id, EntityType.Team, Permission.TEAM_READ):
            raise TeamNotFound()
        return self._list_team_users(team_id)

    @abstractmethod
    def get_default_role(self, default_role: DefaultRole) -> Role:
        raise NotImplementedError

    def grant_entity_role(self, manager: UserID, entity_id: UUID, entity_type: EntityType, user_id: UserID, role: Role):
        if not self.check_entity_permission(manager, entity_id, entity_type, Permission.GRANT_ROLE):
            raise NotEnoughPermissions()
        self._grant_entity_role(entity_id, entity_type, user_id, role)

    @abstractmethod
    def _grant_entity_role(self, entity_id: UUID, entity_type: EntityType, user_id: UserID, role: Role):
        raise NotImplementedError

    def revoke_entity_role(self, manager: UserID, entity_id: UUID, entity_type: EntityType, user_id: UserID):
        if not self.check_entity_permission(manager, entity_id, entity_type, Permission.REVOKE_ROLE):
            raise NotEnoughPermissions()
        if manager == user_id:
            raise NotEnoughPermissions()
        self._revoke_entity_role(entity_id, entity_type, user_id)

    @abstractmethod
    def _revoke_entity_role(self, entity_id: UUID, entity_type: EntityType, user_id: UserID):
        raise NotImplementedError


class ProjectManager(EvidentlyBaseModel):
    metadata: MetadataStorage
    blob: BlobStorage
    data: DataStorage
    auth: AuthManager

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        user_id: UserID = None,
        team_id: TeamID = None,
        org_id: OrgID = None,
    ) -> Project:
        from evidently.ui.dashboards import DashboardConfig

        project = self.add_project(
            Project(
                name=name, description=description, dashboard=DashboardConfig(name=name, panels=[]), team_id=team_id
            ),
            user_id,
            team_id,
            org_id,
        )
        return project

    def add_project(
        self, project: Project, user_id: Optional[UserID], team_id: Optional[TeamID], org_id: Optional[OrgID]
    ) -> Project:
        user = self.auth.get_or_default_user(user_id)
        team = self.auth.get_or_default_team(team_id, user.id)
        project.team_id = team_id
        return self.metadata.add_project(project, user, team).bind(self, user.id)

    def update_project(self, user_id: Optional[UserID], project: Project):
        user = self.auth.get_or_default_user(user_id)
        if not self.auth.check_entity_permission(user.id, project.id, EntityType.Project, Permission.PROJECT_WRITE):
            raise ProjectNotFound()
        return self.metadata.update_project(project)

    def get_project(self, user_id: Optional[UserID], project_id: ProjectID) -> Optional[Project]:
        user = self.auth.get_or_default_user(user_id)
        if not self.auth.check_entity_permission(user.id, project_id, EntityType.Project, Permission.PROJECT_READ):
            raise ProjectNotFound()
        project = self.metadata.get_project(project_id)
        if project is None:
            return None
        return project.bind(self, user.id)

    def delete_project(self, user_id: Optional[UserID], project_id: UUID):
        user = self.auth.get_or_default_user(user_id)
        if not self.auth.check_entity_permission(user.id, project_id, EntityType.Project, Permission.PROJECT_DELETE):
            raise ProjectNotFound()
        return self.metadata.delete_project(project_id)

    def list_projects(self, user_id: Optional[UserID]) -> List[Project]:
        user = self.auth.get_or_default_user(user_id)
        project_ids = self.auth.get_available_project_ids(user.id)
        return [p.bind(self, user.id) for p in self.metadata.list_projects(project_ids)]

    def add_snapshot(self, user_id: Optional[UserID], project_id: UUID, snapshot: Snapshot):
        user = self.auth.get_or_default_user(user_id)
        if not self.auth.check_entity_permission(
            user.id, project_id, EntityType.Project, Permission.PROJECT_SNAPSHOT_ADD
        ):
            raise ProjectNotFound()  # todo: better exception
        blob_id = self.blob.put_snapshot(project_id, snapshot)
        self.metadata.add_snapshot(project_id, snapshot, blob_id)
        self.data.extract_points(project_id, snapshot)

    def delete_snapshot(self, user_id: Optional[UserID], project_id: UUID, snapshot_id: UUID):
        user = self.auth.get_or_default_user(user_id)
        if not self.auth.check_entity_permission(
            user.id, project_id, EntityType.Project, Permission.PROJECT_SNAPSHOT_DELETE
        ):
            raise ProjectNotFound()  # todo: better exception
        # todo
        # self.data.remove_points(project_id, snapshot_id)
        # self.blob.delete_snapshot(project_id, snapshot_id)
        self.metadata.delete_snapshot(project_id, snapshot_id)

    def search_project(self, user_id: Optional[UserID], project_name: str) -> List[Project]:
        user = self.auth.get_or_default_user(user_id)
        project_ids = self.auth.get_available_project_ids(user.id)
        return [p.bind(self, user.id) for p in self.metadata.search_project(project_name, project_ids)]

    def list_snapshots(
        self, user_id: UserID, project_id: ProjectID, include_reports: bool = True, include_test_suites: bool = True
    ) -> List[SnapshotMetadata]:
        if not self.auth.check_entity_permission(user_id, project_id, EntityType.Project, Permission.PROJECT_READ):
            raise NotEnoughPermissions()
        snapshots = self.metadata.list_snapshots(project_id, include_reports, include_test_suites)
        for s in snapshots:
            s.project.bind(self, user_id)
        return snapshots

    def load_snapshot(self, user_id: UserID, project_id: UUID, snapshot: Union[UUID, SnapshotMetadata]) -> Snapshot:
        if isinstance(snapshot, SnapshotID):
            snapshot = self.get_snapshot_metadata(user_id, project_id, snapshot)
        with self.blob.open_blob(snapshot.blob_id) as f:
            return parse_obj_as(Snapshot, json.load(f))

    def get_snapshot_metadata(
        self, user_id: UserID, project_id: ProjectID, snapshot_id: SnapshotID
    ) -> SnapshotMetadata:
        if not self.auth.check_entity_permission(user_id, project_id, EntityType.Project, Permission.PROJECT_READ):
            raise NotEnoughPermissions()
        meta = self.metadata.get_snapshot_metadata(project_id, snapshot_id)
        meta.project.bind(self, user_id)
        return meta

    def reload_snapshots(self, user_id: UserID, project_id: UUID):
        if not self.auth.check_entity_permission(user_id, project_id, EntityType.Project, Permission.PROJECT_READ):
            raise NotEnoughPermissions()
        self.metadata.reload_snapshots(project_id)
