import dataclasses
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

import dynaconf
import pydantic
from dynaconf import LazySettings
from dynaconf.utils.boxing import DynaBox
from litestar.di import Provide
from pydantic import BaseModel
from pydantic import PrivateAttr

from evidently._pydantic_compat import parse_obj_as
from evidently.ui.components.base import SECTION_COMPONENT_TYPE_MAPPING
from evidently.ui.components.base import Component
from evidently.ui.components.base import ServiceComponent
from evidently.ui.components.security import NoSecurityConfig
from evidently.ui.components.security import SecurityComponent
from evidently.ui.components.storage import LocalStorageComponent
from evidently.ui.components.storage import StorageComponent
from evidently.ui.components.telemetry import TelemetryComponent

TConfig = TypeVar("TConfig")


def load_config(config_type: Type[TConfig]):
    def _wrap(box: dict) -> TConfig:
        new_box = _convert_keys(box)
        if pydantic.__version__.startswith("2") and issubclass(
            config_type,
            (pydantic.BaseModel, pydantic.v1.BaseModel),
        ):
            return config_type.parse_obj(new_box)  # type: ignore
        elif pydantic.__version__.startswith("1") and issubclass(config_type, (pydantic.BaseModel,)):
            return config_type.parse_obj(new_box)  # type: ignore
        elif dataclasses.is_dataclass(config_type):
            keys = [k.name for k in dataclasses.fields(config_type)]
        else:
            keys = [k for k in config_type.__annotations__.keys()]
        return config_type(**{k: box.get(k) for k in keys if k in new_box})

    return _wrap


def _convert_keys(box):
    if isinstance(box, (DynaBox, LazySettings)):
        return {k.lower(): _convert_keys(v) for k, v in box.items()}
    return box


class Config(BaseModel):
    security: SecurityComponent
    service: ServiceComponent
    additional_components: Dict[str, Component] = {}

    _components: List[Component] = PrivateAttr(default_factory=list)

    @property
    def components(self) -> List[Component]:
        return [getattr(self, name) for name in self.__fields__ if isinstance(getattr(self, name), Component)] + list(
            self.additional_components.values()
        )

    def get_dependencies(self) -> Dict[str, Provide]:
        res = {}
        for c in self.components:
            res.update(c.get_dependencies())
        return res

    def get_middlewares(self):
        res = []
        for c in self.components:
            res.extend(c.get_middlewares())
        return res


TConfig2 = TypeVar("TConfig2", bound=Config)


def load_config2(config_type: Type[TConfig2], box: dict) -> TConfig2:
    new_box = _convert_keys(box)
    components = []
    named_components = {}
    for section, component_dict in new_box.items():
        if section in config_type.__fields__:
            component = parse_obj_as(config_type.__fields__[section].type_, component_dict)
            named_components[section] = component
        elif section in SECTION_COMPONENT_TYPE_MAPPING:
            component = parse_obj_as(SECTION_COMPONENT_TYPE_MAPPING[section], component_dict)
        else:
            raise ValueError(f"unknown config section {section}")
        components.append(component)

    # todo: we will get validation error if not all components configured, but we can wrap it more nicely
    return config_type(components=components, **named_components)


class LocalConfig(Config):
    security: SecurityComponent = NoSecurityConfig()
    service: ServiceComponent = ServiceComponent()
    storage: StorageComponent = LocalStorageComponent()
    telemetry: TelemetryComponent = TelemetryComponent()


settings = dynaconf.Dynaconf(
    envvar_prefix="EVIDENTLY",
)
