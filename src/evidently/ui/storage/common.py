import os
import uuid
from typing import Callable
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader

from evidently.ui.base import AuthManager
from evidently.ui.base import DefaultRole
from evidently.ui.base import EntityType
from evidently.ui.base import Org
from evidently.ui.base import Permission
from evidently.ui.base import Role
from evidently.ui.base import Team
from evidently.ui.base import User
from evidently.ui.config import SecurityConfig
from evidently.ui.type_aliases import ZERO_UUID
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import TeamID
from evidently.ui.type_aliases import UserID

EVIDENTLY_SECRET_ENV = "EVIDENTLY_SECRET"


class NoUser(User):
    id: UserID = ZERO_UUID
    name: str = ""


class NoTeam(Team):
    id: TeamID = ZERO_UUID
    name = ""


class NoOrg(Org):
    id: OrgID = ZERO_UUID
    name = ""


NO_USER = NoUser()
NO_TEAM = NoTeam()
NO_ORG = NoOrg()


class NoopAuthManager(AuthManager):
    user: ClassVar[User] = NO_USER
    team: ClassVar[Team] = NO_TEAM
    org: ClassVar[Org] = NO_ORG

    def create_org(self, owner: UserID, org: Org):
        return self.org

    def get_org(self, org_id: OrgID) -> Optional[Org]:
        return self.org

    def get_default_role(self, default_role: DefaultRole) -> Role:
        return Role(id=0, name=default_role.value)

    def _grant_entity_role(self, entity_id: UUID, entity_type: EntityType, user_id: UserID, role: Role):
        pass

    def _revoke_entity_role(self, entity_id: UUID, entity_type: EntityType, user_id: UserID):
        pass

    def get_available_project_ids(self, user_id: UserID, org_id: Optional[OrgID]) -> Optional[Set[ProjectID]]:
        return None

    def check_entity_permission(
        self, user_id: UserID, entity_id: uuid.UUID, entity_type: EntityType, permission: Permission
    ) -> bool:
        return True

    def create_user(self, user_id: UserID, name: Optional[str]) -> User:
        return self.user

    def get_user(self, user_id: UserID) -> Optional[User]:
        return self.user

    def get_default_user(self) -> User:
        return self.user

    def create_team(self, author: UserID, team: Team, org_id: OrgID) -> Team:
        return self.team

    def get_team(self, team_id: TeamID) -> Optional[Team]:
        return self.team

    def list_user_teams(self, user_id: UserID, org_id: OrgID) -> List[Team]:
        return []

    def _delete_team(self, team_id: TeamID):
        pass

    def _list_team_users(self, team_id: TeamID) -> List[User]:
        return []


SECRET_HEADER_NAME = "evidently-secret"


class SecretHeaderSecurity(SecurityConfig):
    secret: Optional[str] = None
    secret_env: str = EVIDENTLY_SECRET_ENV

    def get_secret_value(self) -> Optional[str]:
        if self.secret is not None:
            return self.secret
        return os.environ.get(self.secret_env)

    def get_user_id_dependency(self) -> Callable[..., Optional[UserID]]:
        return lambda: None

    def get_is_authorized_dependency(self) -> Callable[..., bool]:
        header = APIKeyHeader(name=SECRET_HEADER_NAME, auto_error=False)

        value = self.get_secret_value()

        def is_authorized(secret: str = Depends(header)):
            return value is not None and secret == value

        return is_authorized
