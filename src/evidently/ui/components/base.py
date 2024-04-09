from abc import ABC
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Type
from typing import TypeVar

from litestar import Litestar
from litestar.di import Provide

from evidently.pydantic_utils import PolymorphicModel
from evidently.ui.utils import parse_json

SECTION_COMPONENT_TYPE_MAPPING: Dict[str, Type["Component"]] = {}


T = TypeVar("T", bound="Component")


class ComponentContext:
    def get_component(self, type_: Type[T]) -> T:
        raise NotImplementedError


class Component(PolymorphicModel, ABC):
    __section__: ClassVar[str] = ""
    # __require__: ClassVar[List[Type["Component"]]] = []

    # def get_requirements(self) -> List[Type["Component"]]:
    #     return self.__require__

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.__section__:
            SECTION_COMPONENT_TYPE_MAPPING[cls.__section__] = cls

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        raise NotImplementedError

    def get_middlewares(self, ctx: ComponentContext):
        return []

    def finalize(self, ctx: ComponentContext, app: Litestar):
        pass


DT = TypeVar("DT")


class FactoryComponent(Component, Generic[DT], ABC):
    dependency_name: ClassVar[str]
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False

    def dependency_factory(self) -> Callable[..., DT]:
        raise NotImplementedError(self.__class__)

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {
            self.dependency_name: Provide(
                self.dependency_factory(), use_cache=self.use_cache, sync_to_thread=self.sync_to_thread
            )
        }


class ServiceComponent(Component):
    host: str = "0.0.0.0"
    port: int = 8000

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        # todo: maybe not put utils here
        return {
            "parsed_json": Provide(parse_json),
        }
