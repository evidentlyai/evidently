from typing import Literal
from typing import Optional

from litestar import Request

from evidently._pydantic_compat import SecretStr
from evidently.ui.security.config import SecurityConfig
from evidently.ui.security.service import SecurityService
from evidently.ui.security.service import User
from evidently.ui.type_aliases import ZERO_UUID


class TokenSecurityConfig(SecurityConfig):
    type: Literal["token"] = "token"
    token: SecretStr


SECRET_HEADER_NAME = "evidently-secret"


default_user = User(id=ZERO_UUID, name="")


class TokenSecurity(SecurityService):
    def __init__(self, config: TokenSecurityConfig):
        self.config = config

    def authenticate(self, request: Request) -> Optional[User]:
        if request.headers.get(SECRET_HEADER_NAME) == self.config.token:
            return default_user
        return None
