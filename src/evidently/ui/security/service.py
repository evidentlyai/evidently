import abc
from typing import Optional

from litestar import Request

from evidently._pydantic_compat import BaseModel
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import UserID


class User(BaseModel):
    id: UserID
    org_id: Optional[OrgID]


class SecurityService:
    @abc.abstractmethod
    def authenticate(self, request: Request) -> Optional[User]:
        raise NotImplementedError()
