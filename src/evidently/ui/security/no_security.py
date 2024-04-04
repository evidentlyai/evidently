from litestar import Request

from ..components.security import NoSecurityConfig
from .service import SecurityService
from .service import User


class NoSecurityService(SecurityService):
    def __init__(self, security_config: NoSecurityConfig):
        self.security_config = security_config

    def authenticate(self, request: Request) -> User:
        return User(id=self.security_config.dummy_user_id, org_id=self.security_config.dummy_org_id)
