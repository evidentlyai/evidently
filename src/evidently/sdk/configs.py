import json
import uuid
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import Descriptor
from evidently.errors import EvidentlyError
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

if TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace

ConfigID = uuid.UUID
ConfigVersionID = uuid.UUID


class ConfigContentType(str, Enum):
    Descriptor = "descriptor"
    RunDescriptorsConfig = "run-descriptors-config"


TConfigValue = TypeVar("TConfigValue")


class ConfigContent(AutoAliasMixin, EvidentlyBaseModel, Generic[TConfigValue]):
    __alias_type__: ClassVar = "config_content"
    __value_class__: ClassVar[Type[TConfigValue]]
    __value_type__: ClassVar[ConfigContentType]

    class Config:
        is_base_type = True

    data: Any

    def get_value(self) -> TConfigValue:
        return parse_obj_as(self.__value_class__, self.data)

    def get_type(self) -> ConfigContentType:
        return self.__value_type__

    @classmethod
    @abstractmethod
    def from_value(cls, value: TConfigValue) -> "ConfigContent":
        raise NotImplementedError()

    def __init_subclass__(cls):
        _CONTENT_TYPE_MAPPING[cls.__value_class__] = cls
        super().__init_subclass__()


_CONTENT_TYPE_MAPPING: Dict[Type, Type[ConfigContent]] = {}


class DescriptorContent(ConfigContent[Descriptor]):
    __value_class__: ClassVar = Descriptor
    __value_type__: ClassVar = ConfigContentType.Descriptor

    @classmethod
    def from_value(cls, value: Descriptor) -> "ConfigContent":
        return DescriptorContent(data=json.loads(value.json()))


class ConfigMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[UserID] = None
    description: Optional[str] = None


class GenericConfig(BaseModel):
    id: ConfigID = ZERO_UUID
    project_id: ProjectID = ZERO_UUID
    name: str
    metadata: ConfigMetadata = ConfigMetadata()


class ConfigVersionMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[UserID] = None
    comment: Optional[str] = None


def _parse_any_to_content(value: Any) -> ConfigContent:
    for base_type, content_type in _CONTENT_TYPE_MAPPING.items():
        if isinstance(value, base_type):
            return content_type.from_value(value)
    raise ValueError(f"Cannot convert {value} to ConfigContent")


class ConfigVersion(BaseModel):
    id: ConfigVersionID = ZERO_UUID
    config_id: ConfigID = ZERO_UUID
    version: int
    metadata: ConfigVersionMetadata = ConfigVersionMetadata()
    content: ConfigContent
    content_type: ConfigContentType

    def __init__(
        self,
        content: Union[Any, ConfigContent],
        version: int,
        id: ConfigVersionID = ZERO_UUID,
        config_id: ConfigID = ZERO_UUID,
        metadata: Optional[ConfigVersionMetadata] = None,
        content_type: Optional[ConfigContentType] = None,
        **data: Any,
    ):
        if not isinstance(content, ConfigContent):
            try:
                content = parse_obj_as(ConfigContent, content)  # type: ignore[type-abstract]
            except ValueError:
                content = _parse_any_to_content(content)

        if content_type is None:
            content_type = content.get_type()
        elif content_type != content.get_type():
            raise ValueError(f"Wrong content type for content {content.__class__.__name__}")

        super().__init__(
            content=content,
            version=version,
            id=id,
            config_id=config_id,
            metadata=metadata or ConfigVersionMetadata(),
            content_type=content_type,
            **data,
        )


VersionOrLatest = Union[int, Literal["latest"]]
T = TypeVar("T")


class RemoteGenericConfig(GenericConfig):
    _manager: "RemoteConfigManager" = PrivateAttr()

    def bind(self, manager: "RemoteConfigManager") -> "RemoteGenericConfig":
        self._manager = manager
        return self

    def list_versions(self) -> List[ConfigVersion]:
        return self._manager.list_versions(self.id)

    def get_version(self, version: VersionOrLatest = "latest") -> ConfigVersion:
        return self._manager.get_version(self.id, version)

    def bump_version(self, content: Any):
        return self._manager.bump_config_version(self.id, content)

    def delete(self):
        return self._manager.delete_config(self.id)

    def delete_version(self, version_id: ConfigVersionID):
        return self._manager.delete_version(version_id)

    def save(self):
        self._manager.update_config(self)


class RemoteConfigManager:
    def __init__(self, workspace: "CloudWorkspace"):
        self._ws = workspace

    def list_configs(self, project_id: ProjectID) -> List[RemoteGenericConfig]:
        return [
            p.bind(self)
            for p in self._ws._request(
                "/api/configs", "GET", query_params={"project_id": project_id}, response_model=List[RemoteGenericConfig]
            )
        ]

    def get_or_create_config(self, project_id: ProjectID, name: str) -> RemoteGenericConfig:
        try:
            return self.get_config(project_id, name)
        except EvidentlyError as e:
            if not e.get_message() == "EvidentlyError: config not found":
                raise e
            return self.create_config(project_id, name)

    def get_config(self, project_id: ProjectID, name: str) -> RemoteGenericConfig:
        return self._ws._request(
            f"/api/configs/by-name/{name}",
            "GET",
            query_params={"project_id": project_id},
            response_model=RemoteGenericConfig,
        ).bind(self)

    def get_config_by_id(self, project_id: ProjectID, config_id: ConfigID) -> RemoteGenericConfig:
        return self._ws._request(f"/api/configs/{config_id}", "GET", response_model=RemoteGenericConfig).bind(self)

    def create_config(self, project_id: ProjectID, name: str) -> RemoteGenericConfig:
        return self._ws._request(
            "/api/configs/",
            "POST",
            query_params={"project_id": project_id},
            body=GenericConfig(name=name, metadata=ConfigMetadata()).dict(),
            response_model=RemoteGenericConfig,
        ).bind(self)

    def delete_config(self, config_id: ConfigID):
        return self._ws._request(f"/api/configs/{config_id}", "DELETE")

    def update_config(self, config: GenericConfig):
        self._ws._request(
            f"/api/configs/{config.id}",
            "PUT",
            body=json.loads(config.json()),
        )

    def list_versions(self, config_id: ConfigID) -> List[ConfigVersion]:
        return self._ws._request(f"/api/configs/{config_id}/versions", "GET", response_model=List[ConfigVersion])

    def get_version(self, config_id: ConfigID, version: VersionOrLatest = "latest") -> ConfigVersion:
        return self._ws._request(f"/api/configs/{config_id}/versions/{version}", "GET", response_model=ConfigVersion)

    def get_version_by_id(self, config_version_id: ConfigVersionID) -> ConfigVersion:
        return self._ws._request(
            f"/api/configs/config-versions/{config_version_id}", "GET", response_model=ConfigVersion
        )

    def create_version(self, config_id: ConfigID, version: int, content: Any) -> ConfigVersion:
        return self._ws._request(
            f"/api/configs/{config_id}/versions",
            "POST",
            body=ConfigVersion(version=version, content=content).dict(),
            response_model=ConfigVersion,
        )

    def delete_version(self, config_version_id: ConfigVersionID):
        self._ws._request(f"/api/configs/config-versions/{config_version_id}", "DELETE")

    def bump_config_version(self, config_id: ConfigID, content: Any) -> ConfigVersion:
        # todo: single request?
        try:
            latest = self.get_version(config_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: config version not found":
                raise e
            version = 1
        return self.create_version(config_id, version, content)

    def _add_typed_version(self, project_id: ProjectID, name: str, value: Any) -> ConfigVersion:
        config = self.get_or_create_config(project_id, name)
        return self.bump_config_version(config.id, value)

    def _get_typed_version(self, project_id: ProjectID, name: str, version: VersionOrLatest, type_: Type[T]) -> T:
        config = self.get_config(project_id, name)
        config_version = self.get_version(config.id, version)
        value = config_version.content.get_value()
        if not isinstance(value, type_):
            raise ValueError(f"Config with name '{name}' is not a {type_.__class__.__name__}")
        return value

    def add_descriptor(self, project_id: ProjectID, name: str, descriptor: Descriptor):
        return self._add_typed_version(project_id, name, descriptor)

    def get_descriptor(self, project_id: ProjectID, name: str, version: VersionOrLatest = "latest") -> Descriptor:
        return self._get_typed_version(project_id, name, version, Descriptor)  # type: ignore[type-abstract]
