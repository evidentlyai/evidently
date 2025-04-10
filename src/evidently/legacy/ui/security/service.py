import abc
from typing import Optional

from litestar import Request

from evidently.legacy.ui.base import User


class SecurityService:
    @abc.abstractmethod
    def authenticate(self, request: Request) -> Optional[User]:
        raise NotImplementedError()
