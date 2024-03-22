import dataclasses
from typing import Type
from typing import TypeVar
from typing import Union

import dynaconf
import pydantic
from dynaconf import LazySettings
from dynaconf.utils.boxing import DynaBox
from pydantic import BaseModel

from evidently.ui.security.config import NoSecurityConfig
from evidently.ui.security.token import TokenSecurityConfig

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


class TelemetryConfig(BaseModel):
    url: str = "http://35.232.253.5:8000/api/v1/s2s/event?ip_policy=strict"
    tool_name: str = "evidently"
    service_name: str = "service"
    token: str = "s2s.5xmxpip2ax4ut5rrihfjhb.uqcoh71nviknmzp77ev6rd"
    enabled: bool = True


class ServiceConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class StorageConfig(BaseModel):
    path: str = "workspace"
    autorefresh: bool = True


class Config(BaseModel):
    service: ServiceConfig = ServiceConfig()
    storage: StorageConfig = StorageConfig()
    security: Union[NoSecurityConfig, TokenSecurityConfig] = NoSecurityConfig()
    telemetry: TelemetryConfig = TelemetryConfig()


settings = dynaconf.Dynaconf(
    envvar_prefix="EVIDENTLY",
)
