from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Set
from typing import Tuple

from evidently._pydantic_compat import BaseModel
from evidently.ui.service.base import EntityType
from evidently.ui.service.base import Org
from evidently.ui.service.base import Team
from evidently.ui.service.base import User
from evidently.ui.service.errors import NotEnoughPermissions
from evidently.ui.service.errors import OrgNotFound
from evidently.ui.service.errors import ProjectNotFound
from evidently.ui.service.errors import TeamNotFound
from evidently.ui.service.type_aliases import EntityID
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import RoleID
from evidently.ui.service.type_aliases import TeamID
from evidently.ui.service.type_aliases import UserID


class Permission(Enum):
    GRANT_ROLE = "all_grant_role"
    REVOKE_ROLE = "all_revoke_role"
    LIST_USERS = "all_list_users"

    ORG_READ = "org_read"
    ORG_WRITE = "org_write"
    ORG_CREATE_TEAM = "org_create_team"
    ORG_DELETE = "org_delete"

    TEAM_READ = "team_read"
    TEAM_WRITE = "team_write"
    TEAM_CREATE_PROJECT = "team_create_project"
    TEAM_DELETE = "team_delete"

    PROJECT_READ = "project_read"
    PROJECT_WRITE = "project_write"
    PROJECT_DELETE = "project_delete"
    PROJECT_SNAPSHOT_ADD = "project_snapshot_add"
    PROJECT_SNAPSHOT_DELETE = "project_snapshot_delete"

    DATASET_READ = "datasets_read"
    DATASET_WRITE = "datasets_write"
    DATASET_DELETE = "datasets_delete"

    UNKNOWN = "unknown"


class Role(BaseModel):
    id: RoleID
    name: str
    entity_type: Optional[EntityType]
    permissions: Set[Permission]


class DefaultRole(Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"
    DEMO_VIEWER = "demo_viewer"


DEFAULT_ROLE_PERMISSIONS: Dict[Tuple[DefaultRole, Optional[EntityType]], Set[Permission]] = {
    (DefaultRole.OWNER, None): set(Permission) - {Permission.UNKNOWN},
    (DefaultRole.EDITOR, EntityType.Org): {
        Permission.LIST_USERS,
        Permission.ORG_READ,
        Permission.ORG_CREATE_TEAM,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.TEAM_CREATE_PROJECT,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.PROJECT_SNAPSHOT_ADD,
        Permission.DATASET_READ,
        Permission.DATASET_WRITE,
        Permission.DATASET_DELETE,
    },
    (DefaultRole.EDITOR, EntityType.Team): {
        Permission.LIST_USERS,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.TEAM_CREATE_PROJECT,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.PROJECT_SNAPSHOT_ADD,
        Permission.DATASET_READ,
        Permission.DATASET_WRITE,
        Permission.DATASET_DELETE,
    },
    (DefaultRole.EDITOR, EntityType.Project): {
        Permission.LIST_USERS,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.PROJECT_SNAPSHOT_ADD,
        Permission.DATASET_READ,
        Permission.DATASET_WRITE,
        Permission.DATASET_DELETE,
    },
    (DefaultRole.EDITOR, EntityType.Dataset): {
        Permission.LIST_USERS,
        Permission.DATASET_READ,
        Permission.DATASET_WRITE,
        Permission.DATASET_DELETE,
    },
    (DefaultRole.VIEWER, EntityType.Org): {
        Permission.LIST_USERS,
        Permission.ORG_READ,
        Permission.PROJECT_READ,
        Permission.DATASET_READ,
    },
    (DefaultRole.VIEWER, EntityType.Team): {
        Permission.LIST_USERS,
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.DATASET_READ,
    },
    (DefaultRole.VIEWER, EntityType.Project): {
        Permission.LIST_USERS,
        Permission.PROJECT_READ,
        Permission.DATASET_READ,
    },
    (DefaultRole.VIEWER, EntityType.Dataset): {
        Permission.LIST_USERS,
        Permission.DATASET_READ,
    },
    (DefaultRole.DEMO_VIEWER, None): {Permission.PROJECT_READ},
}


ENTITY_READ_PERMISSION = {
    EntityType.Org: Permission.ORG_READ,
    EntityType.Team: Permission.TEAM_READ,
    EntityType.Project: Permission.PROJECT_READ,
}

ENTITY_NOT_FOUND_ERROR = {
    EntityType.Org: OrgNotFound,
    EntityType.Team: TeamNotFound,
    EntityType.Project: ProjectNotFound,
}


def get_default_role_permissions(
    default_role: DefaultRole, entity_type: Optional[EntityType]
) -> Tuple[Optional[EntityType], Set[Permission]]:
    res = DEFAULT_ROLE_PERMISSIONS.get((default_role, entity_type))
    if res is None:
        entity_type = None
        res = DEFAULT_ROLE_PERMISSIONS.get((default_role, None))
    if res is None:
        raise ValueError(f"No default role for ({default_role}, {entity_type}) pair")
    return entity_type, res


class UserWithRoles(NamedTuple):
    user: User
    roles: List[Role]


class AuthManager(ABC):
    allow_default_user: bool = True

    async def refresh_default_roles(self):
        for (
            default_role,
            entity_type,
        ), permissions in DEFAULT_ROLE_PERMISSIONS.items():
            role = await self.get_default_role(default_role, entity_type)
            if role.permissions != permissions:
                role.permissions = permissions
                await self.update_role(role)

    @abstractmethod
    async def update_role(self, role: Role):
        raise NotImplementedError

    @abstractmethod
    async def get_available_project_ids(
        self, user_id: UserID, team_id: Optional[TeamID], org_id: Optional[OrgID]
    ) -> Optional[Set[ProjectID]]:
        raise NotImplementedError

    @abstractmethod
    async def check_entity_permission(
        self,
        user_id: UserID,
        entity_type: EntityType,
        entity_id: EntityID,
        permission: Permission,
    ) -> bool:
        raise NotImplementedError

    async def validate_permission(
        self,
        user_id: UserID,
        entity_type: EntityType,
        entity_id: EntityID,
        permission: Permission,
    ):
        if not await self.check_entity_permission(user_id, entity_type, entity_id, permission):
            raise NotEnoughPermissions()

    @abstractmethod
    async def create_user(self, user_id: UserID, name: Optional[str]) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: UserID) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_default_user(self) -> User:
        raise NotImplementedError

    async def get_or_create_user(self, user_id: UserID) -> User:
        user = await self.get_user(user_id)
        if user is None:
            user = await self.create_user(user_id, str(user_id))
        return user

    @abstractmethod
    async def _create_team(self, author: UserID, team: Team, org_id: OrgID) -> Team:
        raise NotImplementedError

    async def create_team(self, author: UserID, team: Team, org_id: OrgID) -> Team:
        if not await self.check_entity_permission(author, EntityType.Org, org_id, Permission.ORG_CREATE_TEAM):
            raise NotEnoughPermissions()
        return await self._create_team(author, team, org_id)

    @abstractmethod
    async def get_team(self, team_id: TeamID) -> Optional[Team]:
        raise NotImplementedError

    async def get_team_or_error(self, team_id: TeamID) -> Team:
        team = await self.get_team(team_id)
        if team is None:
            raise TeamNotFound()
        return team

    @abstractmethod
    async def create_org(self, owner: UserID, org: Org):
        raise NotImplementedError

    @abstractmethod
    async def get_org(self, org_id: OrgID) -> Optional[Org]:
        raise NotImplementedError

    async def delete_org(self, user_id: UserID, org_id: OrgID):
        if not await self.check_entity_permission(user_id, EntityType.Org, org_id, Permission.ORG_DELETE):
            raise NotEnoughPermissions()
        await self._delete_org(org_id)

    @abstractmethod
    async def _delete_org(self, org_id: OrgID):
        raise NotImplementedError

    async def get_org_or_error(self, org_id: OrgID) -> Org:
        org = await self.get_org(org_id)
        if org is None:
            raise OrgNotFound()
        return org

    async def get_or_default_user(self, user_id: UserID) -> User:
        return await self.get_or_create_user(user_id) if user_id is not None else await self.get_default_user()

    @abstractmethod
    async def _delete_team(self, team_id: TeamID):
        raise NotImplementedError

    async def delete_team(self, user_id: UserID, team_id: TeamID):
        if not await self.check_entity_permission(user_id, EntityType.Team, team_id, Permission.TEAM_DELETE):
            raise NotEnoughPermissions()
        await self._delete_team(team_id)

    @abstractmethod
    async def get_default_role(self, default_role: DefaultRole, entity_type: Optional[EntityType]) -> Role:
        raise NotImplementedError

    @abstractmethod
    async def _grant_entity_role(self, entity_type: EntityType, entity_id: EntityID, user_id: UserID, role: Role):
        raise NotImplementedError

    async def grant_entity_role(
        self,
        manager: UserID,
        entity_type: EntityType,
        entity_id: EntityID,
        user_id: UserID,
        role: Role,
        skip_permission_check: bool = False,
    ):
        if not skip_permission_check and not await self.check_entity_permission(
            manager, entity_type, entity_id, Permission.GRANT_ROLE
        ):
            raise NotEnoughPermissions()
        await self._grant_entity_role(entity_type, entity_id, user_id, role)

    @abstractmethod
    async def _revoke_entity_role(self, entity_type: EntityType, entity_id: EntityID, user_id: UserID, role: Role):
        raise NotImplementedError

    async def revoke_entity_role(
        self,
        manager: UserID,
        entity_type: EntityType,
        entity_id: EntityID,
        user_id: UserID,
        role: Role,
    ):
        if not await self.check_entity_permission(manager, entity_type, entity_id, Permission.REVOKE_ROLE):
            raise NotEnoughPermissions()
        if manager == user_id:
            raise NotEnoughPermissions()
        await self._revoke_entity_role(entity_type, entity_id, user_id, role)

    @abstractmethod
    async def _list_entity_users(
        self, entity_type: EntityType, entity_id: EntityID, read_permission: Permission
    ) -> List[User]:
        raise NotImplementedError

    async def list_entity_users(self, user_id: UserID, entity_type: EntityType, entity_id: EntityID):
        if not await self.check_entity_permission(user_id, entity_type, entity_id, Permission.LIST_USERS):
            raise ENTITY_NOT_FOUND_ERROR[entity_type]()
        return await self._list_entity_users(entity_type, entity_id, Permission.LIST_USERS)

    @abstractmethod
    async def _list_entity_users_with_roles(
        self, entity_type: EntityType, entity_id: EntityID, read_permission: Permission
    ) -> List[UserWithRoles]:
        raise NotImplementedError

    async def list_entity_users_with_roles(self, user_id: UserID, entity_type: EntityType, entity_id: EntityID):
        if not await self.check_entity_permission(user_id, entity_type, entity_id, Permission.LIST_USERS):
            raise ENTITY_NOT_FOUND_ERROR[entity_type]()
        return await self._list_entity_users_with_roles(entity_type, entity_id, Permission.LIST_USERS)

    @abstractmethod
    async def list_user_teams(self, user_id: UserID, org_id: Optional[OrgID]) -> List[Team]:
        raise NotImplementedError

    @abstractmethod
    async def list_user_orgs(self, user_id: UserID) -> List[Org]:
        raise NotImplementedError

    @abstractmethod
    async def list_user_entity_permissions(
        self, user_id: UserID, entity_type: EntityType, entity_id: EntityID
    ) -> Set[Permission]:
        raise NotImplementedError

    @abstractmethod
    async def list_user_entity_roles(
        self, user_id: UserID, entity_type: EntityType, entity_id: EntityID
    ) -> List[Tuple[EntityType, EntityID, Role]]:
        raise NotImplementedError

    @abstractmethod
    async def list_roles(self, entity_type: Optional[EntityType]) -> List[Role]:
        raise NotImplementedError
