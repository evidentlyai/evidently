from abc import ABC
from typing import Callable
from typing import ClassVar

from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.components.base import FactoryComponent
from evidently.ui.service.tracing.storage.base import TracingStorage


class TracingStorageComponent(FactoryComponent[TracingStorage], ABC):
    """Base component for tracing storage."""

    class Config:
        is_base_type = True

    __section__: ClassVar[str] = "tracing_storage"
    dependency_name: ClassVar[str] = "tracing_storage"
    use_cache: ClassVar[bool] = True

    def dependency_factory(self) -> Callable[..., TracingStorage]:
        raise NotImplementedError(self.__class__)


class TracingComponent(Component):
    """Component for tracing support."""

    __section__: ClassVar[str] = "tracing"

    def get_api_route_handlers(self, ctx: ComponentContext):
        from evidently.ui.service.components.security import SecurityComponent
        from evidently.ui.service.tracing.api import tracing_api

        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [tracing_api(guard)]
