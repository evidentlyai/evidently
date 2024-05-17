from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from evidently.ui.base import AuthManager
from evidently.ui.base import ProjectPermission
from evidently.ui.base import Team
from evidently.ui.base import TeamPermission
from evidently.ui.base import User
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import ProjectID
from evidently.ui.type_aliases import TeamID
from evidently.ui.type_aliases import UserID

EVIDENTLY_SECRET_ENV = "EVIDENTLY_SECRET"
SECRET_HEADER_NAME = "evidently-secret"


class NoUser(User):
    id: Optional[UserID] = None  # type: ignore[assignment]
    name: str = ""


class NoTeam(Team):
    id: Optional[UserID] = None  # type: ignore[assignment]
    name = ""


NO_USER = NoUser()
NO_TEAM = NoTeam()


class NoopAuthManager(AuthManager):
    user: ClassVar[User] = NO_USER
    team: ClassVar[Team] = NO_TEAM

    def get_available_project_ids(self, user_id: UserID) -> Optional[Set[ProjectID]]:
        return None

    def check_team_permission(self, user_id: UserID, team_id: TeamID, permission: TeamPermission) -> bool:
        return True

    def check_project_permission(self, user_id: UserID, project_id: ProjectID, permission: ProjectPermission) -> bool:
        return True

    def create_user(self, user_id: UserID, name: Optional[str]) -> User:
        return self.user

    def get_user(self, user_id: UserID) -> Optional[User]:
        return self.user

    def get_default_user(self) -> User:
        return self.user

    def create_team(self, author: UserID, team: Team, org_id: Optional[OrgID]) -> Team:
        return self.team

    def get_team(self, team_id: TeamID) -> Optional[Team]:
        return Team(id=team_id, name="")

    def get_default_team(self, user_id: UserID) -> Team:
        return self.team

    def _add_user_to_team(self, team_id: TeamID, user_id: UserID):
        pass

    def _remove_user_from_team(self, team_id: TeamID, user_id: UserID):
        pass

    def _list_user_teams(self, user_id: UserID, include_virtual: bool) -> List[Team]:
        return []

    def _delete_team(self, team_id: TeamID):
        pass

    def _list_team_users(self, team_id: TeamID) -> Dict[UserID, bool]:
        return {}
