from inspect import Parameter
from inspect import Signature
from typing import Any
from typing import Dict
from typing import Type

from litestar.params import Dependency
from typing_extensions import Annotated


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
    def __get__(self, instance, owner: Type["BaseManager"]):
        deps = _get_manager_deps(owner)

        @replace_signature({name: Annotated[cls, Dependency()] for name, cls in deps.items()}, None)
        async def provide(**kwargs):
            obj = owner(**kwargs)
            obj.post_provide()
            return obj

        return provide


class BaseManager:
    provide = ProviderGetter()

    def __init__(self, **dependencies):
        for k, v in dependencies.items():
            setattr(self, k, v)

    def post_provide(self):
        pass


def _get_manager_deps(manager_type: Type[BaseManager]) -> Dict[str, Type]:
    return manager_type.__annotations__
