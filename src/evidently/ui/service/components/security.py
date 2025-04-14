from abc import ABC
from typing import ClassVar
from typing import Dict

import uuid6
from litestar import Request
from litestar.connection import ASGIConnection
from litestar.di import Provide
from litestar.handlers import BaseRouteHandler
from litestar.types import ASGIApp
from litestar.types import Receive
from litestar.types import Scope
from litestar.types import Send

from evidently._pydantic_compat import SecretStr
from evidently.pydantic_utils import register_type_alias
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.errors import NotEnoughPermissions
from evidently.ui.service.security.service import SecurityService
from evidently.ui.service.storage.common import NoopAuthManager
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import UserID


class SecurityComponent(Component, ABC):
    add_security_middleware: ClassVar[bool] = True

    class Config:
        is_base_type = True

    def get_security(self) -> SecurityService:
        raise NotImplementedError

    def get_security_middleware(self, ctx: ComponentContext):
        security = self.get_security()

        def auth_middleware_factory(app: ASGIApp) -> ASGIApp:
            async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
                request: Request = Request(scope)
                auth = security.authenticate(request)
                if auth is None:
                    scope["auth"] = {
                        "authenticated": False,
                    }
                else:
                    scope["auth"] = {
                        "user_id": auth.id,
                        "authenticated": True,
                    }
                await app(scope, receive, send)

            return middleware

        return auth_middleware_factory

    def get_middlewares(self, ctx: ComponentContext):
        if self.add_security_middleware:
            return [self.get_security_middleware(ctx)]
        return []

    def get_auth_guard(self):
        def is_authenticated(connection: ASGIConnection, _: BaseRouteHandler) -> None:
            if not connection.scope["auth"]["authenticated"]:
                raise NotEnoughPermissions()

        return is_authenticated


register_type_alias(SecurityComponent, "evidently.ui.service.components.security.NoSecurityComponent", "none")
register_type_alias(SecurityComponent, "evidently.ui.service.components.security.TokenSecurityComponent", "token")


async def get_user_id() -> UserID:
    return ZERO_UUID


class SimpleSecurity(SecurityComponent):
    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {
            "user_id": Provide(get_user_id),
            "security": Provide(self.get_security, sync_to_thread=False, use_cache=True),
            "security_config": Provide(lambda: self, sync_to_thread=False, use_cache=True),
            "auth_manager": Provide(lambda: NoopAuthManager(), sync_to_thread=False, use_cache=True),
        }


class NoSecurityComponent(SimpleSecurity):
    class Config:
        type_alias = "none"

    dummy_user_id: UserID = uuid6.UUID(int=1, version=7)
    dummy_org_id: OrgID = uuid6.UUID(int=2, version=7)

    def get_security(self) -> SecurityService:
        from evidently.ui.service.security.no_security import NoSecurityService

        return NoSecurityService(self)


class TokenSecurityComponent(SimpleSecurity):
    class Config:
        type_alias = "token"

    token: SecretStr

    def get_security(self) -> SecurityService:
        from evidently.ui.service.security.token import TokenSecurity

        return TokenSecurity(self)
