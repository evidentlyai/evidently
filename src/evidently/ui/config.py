import os.path
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Optional

import yaml

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.ui.base import ProjectManager
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import UserID


class TelemetryConfig(BaseModel):
    url: str = "http://35.232.253.5:8000/api/v1/s2s/event?ip_policy=strict"
    tool_name: str = "evidently"
    service_name: str = "service"
    token: str = "s2s.5xmxpip2ax4ut5rrihfjhb.uqcoh71nviknmzp77ev6rd"
    enabled: bool = True


class ServiceConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class SecurityConfig(EvidentlyBaseModel):
    @abstractmethod
    def get_user_id_dependency(self) -> Callable[..., Optional[UserID]]:
        raise NotImplementedError

    def get_org_id_dependency(self) -> Callable[..., Optional[OrgID]]:
        return lambda: None

    def get_is_authorized_dependency(self) -> Callable[..., bool]:
        get_user_id = self.get_user_id_dependency()

        from fastapi import Depends

        def is_authorized(user_id: Optional[UserID] = Depends(get_user_id)):
            return user_id is not None

        return is_authorized


class NoSecurityConfig(SecurityConfig):
    def get_user_id_dependency(self) -> Callable[..., Optional[UserID]]:
        return lambda: None

    def get_is_authorized_dependency(self) -> Callable[..., bool]:
        return lambda: True


class StorageConfig(EvidentlyBaseModel, ABC):
    @abstractmethod
    def create_project_manager(self) -> ProjectManager:
        raise NotImplementedError


def _default_storage():
    from evidently.ui.storage.local import LocalStorageConfig

    return LocalStorageConfig(path="workspace", autorefresh=True)


class Configuration(BaseModel):
    service: ServiceConfig = Field(default_factory=ServiceConfig)
    telemetry: TelemetryConfig = Field(default_factory=TelemetryConfig)
    storage: StorageConfig = Field(default_factory=_default_storage)
    security: SecurityConfig = NoSecurityConfig()

    @classmethod
    def read(cls, path: str) -> Optional["Configuration"]:
        return read_configuration(path)


def read_configuration(path: str) -> Optional[Configuration]:
    if not os.path.exists(path):
        return None
    with open(path) as f:
        dict_obj = yaml.load(f, yaml.SafeLoader)
        _configuration = Configuration.parse_obj(dict_obj)
    return _configuration
