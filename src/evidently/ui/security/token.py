import uuid
from typing import Literal
from typing import Optional

from litestar import Request

from evidently._pydantic_compat import SecretStr
from evidently.ui.security.config import SecurityConfig
from evidently.ui.security.service import SecurityService
from evidently.ui.security.service import User


class TokenSecurityConfig(SecurityConfig):
    type: Literal["token"] = "token"
    token: SecretStr


SECRET_HEADER_NAME = "evidently-secret"


default_user = User(
    id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
    org_id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
)


class TokenSecurity(SecurityService):
    def __init__(self, config: TokenSecurityConfig):
        self.config = config

    def authenticate(self, request: Request) -> Optional[User]:
        if request.headers.get(SECRET_HEADER_NAME) == self.config.token:
            return default_user
        return None
