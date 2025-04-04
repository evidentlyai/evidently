from abc import ABC
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from litestar import Litestar
from litestar import Router
from litestar.di import Provide
from litestar.types import ControllerRouterHandler
from litestar.types import ExceptionHandlersMap
from litestar.types import Middleware

from evidently._pydantic_compat import Extra
from evidently.legacy.ui.utils import parse_json
from evidently.pydantic_utils import PolymorphicModel

SECTION_COMPONENT_TYPE_MAPPING: Dict[str, Type["Component"]] = {}


T = TypeVar("T", bound="Component")


class AppBuilder:
    def __init__(self, context: "ComponentContext"):
        self.context = context
        self.dependencies: Dict[str, Provide] = {}
        self.route_handlers: List[ControllerRouterHandler] = []
        self.api_route_handlers: List[ControllerRouterHandler] = []
        self.exception_handlers: ExceptionHandlersMap = {}
        self.middlewares: List[Middleware] = []
        self.type_decoders: List[tuple[Callable[[Any], bool], Callable[[Any, Any], Any]]] = []
        self.kwargs: Dict[str, Any] = {}

    def build_api_router(self):
        return Router(path="/api", route_handlers=self.api_route_handlers)

    def build(self) -> Litestar:
        api_router = self.build_api_router()
        return Litestar(
            route_handlers=[api_router] + self.route_handlers,
            exception_handlers=self.exception_handlers,
            dependencies=self.dependencies,
            middleware=self.middlewares,
            type_decoders=self.type_decoders,
            **self.kwargs,
        )


class ComponentContext:
    def get_component(self, type_: Type[T]) -> T:
        raise NotImplementedError


class Component(PolymorphicModel, ABC):
    __section__: ClassVar[str] = ""
    __require__: ClassVar[List[Type["Component"]]] = []
    __priority__: ClassVar[int] = 0
    priority: Optional[int] = None

    def get_priority(self) -> int:
        return self.priority if self.priority is not None else self.__priority__

    def get_requirements(self) -> List[Type["Component"]]:
        return self.__require__

    class Config:
        extra = Extra.forbid
        alias_required = False
        is_base_type = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.__section__:
            SECTION_COMPONENT_TYPE_MAPPING[cls.__section__] = cls

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {}

    def get_middlewares(self, ctx: ComponentContext):
        return []

    def get_route_handlers(self, ctx: ComponentContext):
        return []

    def get_api_route_handlers(self, ctx: ComponentContext):
        return []

    def apply(self, ctx: ComponentContext, builder: AppBuilder):
        builder.dependencies.update(self.get_dependencies(ctx))
        builder.middlewares.extend(self.get_middlewares(ctx))
        builder.route_handlers.extend(self.get_route_handlers(ctx))
        builder.api_route_handlers.extend(self.get_api_route_handlers(ctx))

    def finalize(self, ctx: ComponentContext, app: Litestar):
        pass


DT = TypeVar("DT")


class FactoryComponent(Component, Generic[DT], ABC):
    dependency_name: ClassVar[str]
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[Optional[bool]] = False

    def dependency_factory(self) -> Callable[..., DT]:
        raise NotImplementedError(self.__class__)

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        return {
            self.dependency_name: Provide(
                self.dependency_factory(), use_cache=self.use_cache, sync_to_thread=self.sync_to_thread
            )
        }


class ServiceComponent(Component):
    host: str = "127.0.0.1"
    port: int = 8000

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        # todo: maybe not put utils here
        return {
            "parsed_json": Provide(parse_json, sync_to_thread=False),
        }
