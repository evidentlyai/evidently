from typing import ClassVar
from typing import Dict
from typing import List
from typing import Type

from litestar.di import Provide

from evidently.pydantic_utils import PolymorphicModel
from evidently.ui.utils import parse_json

SECTION_COMPONENT_TYPE_MAPPING: Dict[str, Type["Component"]] = {}


class Component(PolymorphicModel):
    __section__: ClassVar[str] = ""
    __requiers__: ClassVar[List[Type["Component"]]] = []

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.__section__:
            SECTION_COMPONENT_TYPE_MAPPING[cls.__section__] = cls

    def get_dependencies(self) -> Dict[str, Provide]:
        raise NotImplementedError

    def get_middlewares(self):
        return []


class ServiceComponent(Component):
    host: str = "0.0.0.0"
    port: int = 8000

    def get_dependencies(self) -> Dict[str, Provide]:
        # todo: maybe not put utils here
        return {
            "parsed_json": Provide(parse_json),
        }
