import itertools
import os
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from evidently._pydantic_compat import SHAPE_DICT
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import ModelMetaclass
from evidently._pydantic_compat import import_string

if TYPE_CHECKING:
    from evidently._pydantic_compat import DictStrAny
    from evidently._pydantic_compat import Model
T = TypeVar("T")


def pydantic_type_validator(type_: Type[Any]):
    def decorator(f):
        from evidently._pydantic_compat import _VALIDATORS

        for cls, validators in _VALIDATORS:
            if cls is type_:
                validators.append(f)
                return

        _VALIDATORS.append(
            (type_, [f]),
        )

    return decorator


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


ALLOWED_TYPE_PREFIXES = ["evidently."]

EVIDENTLY_TYPE_PREFIXES_ENV = "EVIDENTLY_TYPE_PREFIXES"
ALLOWED_TYPE_PREFIXES.extend([p for p in os.environ.get(EVIDENTLY_TYPE_PREFIXES_ENV, "").split(",") if p])

TYPE_ALIASES: Dict[str, Type["PolymorphicModel"]] = {}


class PolymorphicModel(BaseModel):
    class Config:
        type_alias: ClassVar[Optional[str]] = None

    @classmethod
    def __get_type__(cls):
        config = cls.__dict__.get("Config")
        if config is not None and config.__dict__.get("type_alias") is not None:
            return config.type_alias
        return f"{cls.__module__}.{cls.__name__}"

    type: str = Field("")

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls == PolymorphicModel:
            return
        typename = cls.__get_type__()
        cls.__fields__["type"].default = typename
        TYPE_ALIASES[typename] = cls

    @classmethod
    def __subtypes__(cls):
        return Union[tuple(all_subclasses(cls))]

    @classmethod
    def validate(cls: Type["Model"], value: Any) -> "Model":
        if isinstance(value, dict) and "type" in value:
            typename = value.pop("type")
            if typename in TYPE_ALIASES:
                subcls = TYPE_ALIASES[typename]
            else:
                if not any(typename.startswith(p) for p in ALLOWED_TYPE_PREFIXES):
                    raise ValueError(f"{typename} does not match any allowed prefixes")
                subcls = import_string(typename)
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
    def _to_enum_value(self, key, value):
        field = self.__fields__[key]
        if not issubclass(field.type_, Enum):
            return value
        if isinstance(value, list):
            return [v.value if isinstance(v, Enum) else v for v in value]
        return value.value if isinstance(value, Enum) else value

    def dict(self, *args, **kwargs) -> "DictStrAny":
        res = super().dict(*args, **kwargs)
        return {k: self._to_enum_value(k, v) for k, v in res.items()}


class ExcludeNoneMixin(BaseModel):
    def dict(self, *args, **kwargs) -> "DictStrAny":
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)


class FieldPath:
    def __init__(self, path: List[str], cls: Type, is_mapping: bool = False):
        self._path = path
        self._cls = cls
        self._is_mapping = is_mapping

    def list_fields(self) -> List[str]:
        if issubclass(self._cls, BaseModel):
            return list(self._cls.__fields__)
        return []

    def __getattr__(self, item) -> "FieldPath":
        if self._is_mapping:
            return FieldPath(self._path + [item], self._cls)
        if not issubclass(self._cls, BaseModel):
            raise AttributeError(f"{self._cls} does not have fields")
        if item not in self._cls.__fields__:
            raise AttributeError(f"{self._cls} type does not have '{item}' field")
        field = self._cls.__fields__[item]
        return FieldPath(self._path + [item], field.type_, is_mapping=field.shape == SHAPE_DICT)

    def list_nested_fields(self) -> List[str]:
        if not isinstance(self._cls, type) or not issubclass(self._cls, BaseModel):
            return [repr(self)]
        res = []
        for name, field in self._cls.__fields__.items():
            if field.shape == SHAPE_DICT:
                name = f"{name}.*"
            res.extend(FieldPath(self._path + [name], field.type_).list_nested_fields())
        return res

    def __repr__(self):
        return self.get_path()

    def get_path(self):
        return ".".join(self._path)

    def __dir__(self) -> Iterable[str]:
        res: List[str] = []
        res.extend(super().__dir__())
        res.extend(self.list_fields())
        return res


@pydantic_type_validator(FieldPath)
def series_validator(value):
    return value.get_path()
