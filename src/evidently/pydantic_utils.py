import itertools
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.main import ModelMetaclass
from pydantic.utils import import_string

if TYPE_CHECKING:
    from pydantic.main import Model
    from pydantic.typing import DictStrAny
T = TypeVar("T")


class FrozenBaseMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        res = super().__new__(mcs, name, bases, namespace, **kwargs)
        res.__config__.frozen = True
        return res


object_setattr = object.__setattr__
object_delattr = object.__delattr__


class FrozenBaseModel(BaseModel, metaclass=FrozenBaseMeta):
    class Config:
        underscore_attrs_are_private = True

    _init_values: Optional[Dict]

    def __init__(self, **data: Any):
        super().__init__(**self.__init_values__, **data)
        for private_attr in self.__private_attributes__:
            if private_attr in self.__init_values__:
                object_setattr(self, private_attr, self.__init_values__[private_attr])
        object_setattr(self, "_init_values", None)

    @property
    def __init_values__(self):
        if not hasattr(self, "_init_values"):
            object_setattr(self, "_init_values", {})
        return self._init_values

    def __setattr__(self, key, value):
        if self.__init_values__ is not None:
            if key not in self.__fields__ and key not in self.__private_attributes__:
                raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")
            self.__init_values__[key] = value
            return
        super().__setattr__(key, value)

    def __hash__(self):
        try:
            return hash(self.__class__) + hash(tuple(self._field_hash(v) for v in self.__dict__.values()))
        except TypeError:
            raise

    @classmethod
    def _field_hash(cls, value):
        if isinstance(value, list):
            return tuple(cls._field_hash(v) for v in value)
        if isinstance(value, dict):
            return tuple((k, cls._field_hash(v)) for k, v in value.items())
        return value


def all_subclasses(cls: Type[T]) -> Set[Type[T]]:
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


class PolymorphicModel(BaseModel):
    @classmethod
    def __get_type__(cls):
        return f"{cls.__module__}.{cls.__name__}"

    type: str = Field("")

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls == PolymorphicModel:
            return
        cls.__fields__["type"].default = cls.__get_type__()

    @classmethod
    def __subtypes__(cls):
        return Union[tuple(all_subclasses(cls))]

    @classmethod
    def validate(cls: Type["Model"], value: Any) -> "Model":
        if isinstance(value, dict) and "type" in value:
            subcls = import_string(value.pop("type"))
            return subcls.validate(value)
        return super().validate(value)  # type: ignore[misc]


class EvidentlyBaseModel(FrozenBaseModel, PolymorphicModel):
    pass


class WithTestAndMetricDependencies(EvidentlyBaseModel):
    def __evidently_dependencies__(self):
        from evidently.base_metric import Metric
        from evidently.tests.base_test import Test

        for field_name, field in itertools.chain(
            self.__dict__.items(), ((pa, getattr(self, pa, None)) for pa in self.__private_attributes__)
        ):
            if issubclass(type(field), (Metric, Test)):
                yield field_name, field


class EnumValueMixin(BaseModel):
    def dict(self, *args, **kwargs) -> "DictStrAny":
        res = super().dict(*args, **kwargs)
        return {k: v.value if isinstance(v, Enum) else v for k, v in res.items()}


class ExcludeNoneMixin(BaseModel):
    def dict(self, *args, **kwargs) -> "DictStrAny":
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)
