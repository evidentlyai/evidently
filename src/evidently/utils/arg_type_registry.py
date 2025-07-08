from collections import defaultdict
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

_registry: Dict[Type, Dict[str, Type]] = defaultdict(dict)

T = TypeVar("T", bound="BaseArgTypeRegistry")


class BaseArgTypeRegistry:
    __registry_alias__: ClassVar[Optional[str]] = None

    @classmethod
    def _get_base_type(cls):
        from evidently.pydantic_utils import PolymorphicModel
        from evidently.pydantic_utils import get_base_class

        if issubclass(cls, PolymorphicModel):
            return get_base_class(cls)
        base = cls
        for c in cls.mro():
            if c is BaseArgTypeRegistry:
                break
            base = c
        return base

    def __init_subclass__(cls):
        base_class = cls._get_base_type()
        if cls.__registry_alias__ is not None:
            _registry[base_class][cls.__registry_alias__] = cls
        super().__init_subclass__()

    @classmethod
    def registry_lookup(cls: Type[T], name_or_instance: Union[str, T]) -> T:
        if isinstance(name_or_instance, str):
            base = cls._get_base_type()
            try:
                type_ = _registry[base][name_or_instance]
                return type_()
            except KeyError:
                raise KeyError(f"{name_or_instance} not registered")
        if isinstance(name_or_instance, cls):
            return name_or_instance
        raise NotImplementedError(f"{name_or_instance} not registered")
