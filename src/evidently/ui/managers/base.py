from inspect import Parameter
from inspect import Signature
from typing import Any
from typing import Dict
from typing import Type

from litestar.params import Dependency
from typing_extensions import Annotated
from typing_inspect import is_classvar


def replace_signature(annotations: Dict[str, Any], return_annotation=..., is_method=False):
    """Decorator to trick Litestar DI into providing arguments needed"""

    def dec(f):
        parameters = [Parameter(n, kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=t) for n, t in annotations.items()]
        if is_method:
            parameters.insert(0, Parameter("self", kind=Parameter.POSITIONAL_OR_KEYWORD))
        f.__signature__ = Signature(parameters=parameters, return_annotation=return_annotation)
        f.__annotations__ = annotations
        f.__annotations__["return"] = return_annotation
        return f

    return dec


class ProviderGetter:
    def __get__(self, instance, owner: Type["BaseDependant"]):
        deps = _get_manager_deps(owner)

        @replace_signature({name: Annotated[cls, Dependency(skip_validation=True)] for name, cls in deps.items()}, None)
        async def provide(**kwargs):
            obj = owner(**kwargs)
            await obj.post_provide()
            return obj

        provide.__name__ = f"{owner.__name__}.provide"
        return provide


class BaseDependant:
    """Base class that allows to define dependencies as class fields"""

    provide = ProviderGetter()

    def __init__(self, **dependencies):
        for k, v in dependencies.items():
            setattr(self, k, v)

    async def post_provide(self):
        pass


def _get_manager_deps(dependant_type: Type[BaseDependant]) -> Dict[str, Type]:
    return {
        name: cls
        for bt in dependant_type.mro()
        if issubclass(bt, BaseDependant)
        for name, cls in bt.__annotations__.items()
        if not is_classvar(cls)
    }


class BaseManager(BaseDependant):
    pass
