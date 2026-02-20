import dataclasses
import hashlib
import inspect
import itertools
import json
import os
import warnings
from abc import ABC
from enum import Enum
from functools import lru_cache
from typing import Annotated
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import FrozenSet
from typing import Iterable
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin

import numpy as np
import yaml
from pydantic import BaseModel
from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import Field
from pydantic import GetCoreSchemaHandler
from pydantic import TypeAdapter
from pydantic import model_serializer
from pydantic import model_validator
from pydantic._internal._model_construction import ModelMetaclass
from pydantic._internal._validators import import_string
from pydantic.fields import FieldInfo as PydanticFieldInfo
from pydantic_core import PydanticCustomError
from pydantic_core import core_schema
from pydantic_core.core_schema import SerializationInfo
from pydantic_core.core_schema import SerializerFunctionWrapHandler
from typing_extensions import Self
from typing_inspect import is_union_type


def _is_dict_annotation(annotation: Any) -> bool:
    """True if the field annotation is dict-like (Dict, dict, Mapping)."""
    origin = get_origin(annotation)
    if origin is None:
        return annotation is dict
    return origin is dict or (hasattr(origin, "__origin__") and origin.__name__ == "Mapping")


def _get_dict_value_type(annotation: Any) -> Any:
    """Get the value type from a Dict[K, V] annotation, unwrapping Annotated if needed."""
    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    args = get_args(annotation)
    if len(args) >= 2:
        return args[1]
    return None


md5_kwargs = {"usedforsecurity": False}


T = TypeVar("T")


def pydantic_type_validator(type_: Type[Any]):
    """
    Decorator to register a validator function for a type in Pydantic v2.

    Args:
        type_: The type to register the validator for (e.g., pd.Series)

    Example:
        @pydantic_type_validator(pd.Series)
        def validate_series(v: Any) -> pd.Series:
            if isinstance(v, pd.Series):
                return v
            if isinstance(v, list):
                return pd.Series(v)
            raise ValueError(f"Cannot convert {type(v)} to pd.Series")
    """

    def decorator(validator_func: Callable[[Any], Any]):
        def _get_pydantic_core_schema(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            return core_schema.no_info_plain_validator_function(validator_func)

        # Monkey-patch the type
        type_.__get_pydantic_core_schema__ = classmethod(_get_pydantic_core_schema)

        return validator_func

    return decorator


class FrozenBaseMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        res: Type[BaseModel] = super().__new__(mcs, name, bases, namespace, **kwargs)
        res.model_config["frozen"] = True
        return res


object_setattr = object.__setattr__
object_delattr = object.__delattr__


class FrozenBaseModel(BaseModel, metaclass=FrozenBaseMeta):
    model_config = ConfigDict()

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
            if key not in self.model_fields and key not in self.__private_attributes__:
                raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")
            self.__init_values__[key] = value
            return
        super().__setattr__(key, value)

    def __hash__(self):
        try:
            return hash(self.__class__) + hash(
                tuple(self._field_hash(v) for k, v in self.__dict__.items() if k in self.model_fields)
            )
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

TYPE_ALIASES: Dict[Tuple[Type["PolymorphicModel"], str], str] = {}
LOADED_TYPE_ALIASES: Dict[Tuple[Type["PolymorphicModel"], str], Type["PolymorphicModel"]] = {}


def register_type_alias(base_class: Type["PolymorphicModel"], classpath: str, alias: str):
    while True:
        key = (base_class, alias)

        if key in TYPE_ALIASES and TYPE_ALIASES[key] != classpath and "PYTEST_CURRENT_TEST" not in os.environ:
            warnings.warn(f"Duplicate key {key} in alias map")
        TYPE_ALIASES[key] = classpath

        if base_class is PolymorphicModel:
            break
        base_class = get_base_class(base_class, ensure_parent=True)  # type: ignore[arg-type]
        if not getattr(base_class, "__transitive_aliases__", False):
            break


def autoregister(cls: Type["PolymorphicModel"]):
    """Decorator that automatically registers subclass.
    Can only be used on subclasses that are defined in the same file as base class
    (or if the import of this subclass is guaranteed when base class is imported)
    """
    register_type_alias(get_base_class(cls), get_classpath(cls), cls.__get_type__())  # type: ignore[arg-type]
    return cls


def register_loaded_alias(base_class: Type["PolymorphicModel"], cls: Type["PolymorphicModel"], alias: str):
    if not issubclass(cls, base_class):
        raise ValueError(f"Cannot register alias: {cls.__name__} is not subclass of {base_class.__name__}")

    key = (base_class, alias)
    if key in LOADED_TYPE_ALIASES and LOADED_TYPE_ALIASES[key] != cls and "PYTEST_CURRENT_TEST" not in os.environ:
        warnings.warn(f"Duplicate key {key} in alias map")
    LOADED_TYPE_ALIASES[key] = cls


@lru_cache()
def get_base_class(cls: Type["PolymorphicModel"], ensure_parent: bool = False) -> Type["PolymorphicModel"]:
    for cls_ in cls.mro():
        if ensure_parent and cls_ is cls:
            continue
        if not issubclass(cls_, PolymorphicModel):
            continue
        if cls_.__dict__.get("__is_base_type__", False):
            return cls_
    return PolymorphicModel


def get_classpath(cls: Type) -> str:
    return f"{cls.__module__}.{cls.__name__}"


TPM = TypeVar("TPM", bound="PolymorphicModel")

Fingerprint = str
FingerprintPart = Union[None, int, str, float, bool, bytes, Tuple["FingerprintPart", ...]]


def is_not_abstract(cls):
    return not (inspect.isabstract(cls) or ABC in cls.__bases__)


class PolymorphicModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Configuration values
    __type_alias__: ClassVar[Optional[str]] = None
    __alias_required__: ClassVar[bool] = True
    # __transitive_aliases__: ClassVar[bool] = False
    __is_base_type__: ClassVar[bool] = False

    type: str = Field(default="")

    @classmethod
    def __get_type__(cls) -> str:
        type_alias = cls.__dict__.get("__type_alias__")
        if type_alias is not None:
            return str(type_alias)
        if cls.__alias_required__ and is_not_abstract(cls):
            raise ValueError(f"Alias is required for {cls.__name__}")
        return cls.__get_classpath__()

    @classmethod
    def __get_classpath__(cls):
        return get_classpath(cls)

    @classmethod
    def __subtypes__(cls) -> Tuple[Type["PolymorphicModel"], ...]:
        return tuple(all_subclasses(cls))

    @classmethod
    def __get_is_base_type__(cls) -> bool:
        return cls.__dict__.get("__is_base_type__", False)

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls == PolymorphicModel or cls.__get_is_base_type__():
            return

        typename = cls.__get_type__()
        literal_typename = Literal[typename]

        cls.__annotations__["type"] = literal_typename
        if "type" not in cls.__dict__:
            cls.type = typename

        base_class = get_base_class(cls)
        if (base_class, typename) not in LOADED_TYPE_ALIASES:
            register_loaded_alias(base_class, cls, typename)
        if base_class != cls:
            base_typefield = base_class.model_fields.get("type")
            if base_typefield is not None:
                base_typefield_type = base_typefield.annotation
                if is_union_type(base_typefield_type):
                    subclass_literals = get_args(base_typefield_type) + (literal_typename,)
                else:
                    subclass_literals = (base_typefield_type, literal_typename)
                base_class.__annotations__["type"] = Union[subclass_literals]

    def __str__(self):
        return f"{self.__class__.__name__}[{self.__get_type__()}]({super().__str__()})"

    @classmethod
    def model_validate(
        cls,
        value: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
    ) -> Self:
        if isinstance(value, dict) and "type" in value:
            typename = value.pop("type")
            try:
                subcls = cls.load_alias(typename)
                return subcls.model_validate(
                    value, strict=strict, from_attributes=from_attributes, context=context
                )  # Pydantic v2 uses model_validate
            finally:
                value["type"] = typename
        return super().model_validate(value, strict=strict, from_attributes=from_attributes, context=context)

    @model_validator(mode="wrap")
    def _delegate_validation(cls, data, handler) -> Any:
        if not isinstance(data, dict):
            return handler(data)
        if "type" in data and data["type"] != cls.__get_type__():
            return cls.model_validate(data)
        typename = data.pop("type", None) if isinstance(data, dict) else None
        try:
            return handler(data)
        finally:
            if typename is not None:
                data["type"] = typename

        # if "type" in data and data["type"] != cls.__get_type__():
        #     return cls.model_validate(data)
        # try:
        #     return handler(data)
        # except TypeError as e:
        #     raise

    @model_serializer(mode="wrap")
    def _delegate_serialization(self, nxt: SerializerFunctionWrapHandler, info: SerializationInfo):
        if f"serializer={self.__class__.__name__}" not in str(nxt):
            return self.model_dump(  # type: ignore[call-arg]
                mode=info.mode,
                include=info.include,  # type: ignore[arg-type]
                exclude=info.exclude,  # type: ignore[arg-type]
                context=info.context,
                by_alias=info.by_alias,
                exclude_unset=info.exclude_unset,
                exclude_none=info.exclude_none,
                exclude_defaults=info.exclude_defaults,
                round_trip=info.round_trip,  # type: ignore[arg-type]
                serialize_as_any=info.serialize_as_any,
            )
        return nxt(self)

    @classmethod
    def load_alias(cls, typename: str):
        key = (get_base_class(cls), typename)

        if key in LOADED_TYPE_ALIASES:
            subcls = LOADED_TYPE_ALIASES[key]
        else:
            if key in TYPE_ALIASES:
                classpath = TYPE_ALIASES[key]
            else:
                if "." not in typename:
                    raise PydanticCustomError("unknown_alias", f'Unknown alias "{typename}"')
                classpath = typename
            if not any(classpath.startswith(p) for p in ALLOWED_TYPE_PREFIXES):
                raise PydanticCustomError("invalid_prefix", f"{classpath} does not match any allowed prefixes")
            try:
                subcls = import_string(classpath)
            except ImportError as e:
                raise PydanticCustomError("import_error", f"Error importing subclass from '{classpath}'") from e
        return subcls


def get_value_fingerprint(value: Any) -> FingerprintPart:
    if isinstance(value, EvidentlyBaseModel):
        return value.get_fingerprint()
    if isinstance(value, np.int64):
        return int(value)
    if isinstance(value, BaseModel):
        return get_value_fingerprint(value.model_dump())
    if dataclasses.is_dataclass(value):
        return get_value_fingerprint(dataclasses.asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    if isinstance(value, dict):
        return tuple((get_value_fingerprint(k), get_value_fingerprint(v)) for k, v in sorted(value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(get_value_fingerprint(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return tuple(get_value_fingerprint(v) for v in sorted(value, key=str))
    if isinstance(value, Callable):  # type: ignore
        return hash(value)
    raise NotImplementedError(
        f"Not implemented for value of type {value.__class__.__module__}.{value.__class__.__name__}"
    )


EBM = TypeVar("EBM", bound="EvidentlyBaseModel")


def _is_yaml_fmt(path: str, fmt: Literal["yaml", "json", None]) -> bool:
    if fmt == "yaml":
        return True
    if fmt == "json":
        return False
    return path.endswith(".yml") or path.endswith(".yaml")


class EvidentlyBaseModel(FrozenBaseModel, PolymorphicModel):
    __type_alias__: ClassVar[Optional[str]] = "evidently:base:EvidentlyBaseModel"
    __alias_required__: ClassVar[bool] = True
    __is_base_type__: ClassVar[bool] = True

    def get_fingerprint(self) -> Fingerprint:
        classpath = self.__get_classpath__()
        if ".legacy" in classpath:
            classpath = classpath.replace(".legacy", "")
        return hashlib.md5((classpath + str(self.get_fingerprint_parts())).encode("utf8"), **md5_kwargs).hexdigest()

    def get_fingerprint_parts(self) -> Tuple[FingerprintPart, ...]:
        return tuple(
            (name, self.get_field_fingerprint(name))
            for name, field in sorted(self.model_fields.items())
            if field.is_required() or getattr(self, name) != field.default
        )

    def get_field_fingerprint(self, field: str) -> FingerprintPart:
        value = getattr(self, field)
        return get_value_fingerprint(value)

    def update(self: EBM, **kwargs) -> EBM:
        data = self.model_dump()
        data.update(kwargs)
        return self.__class__(**data)

    @classmethod
    def load(cls: Type[EBM], path: str, fmt: Literal["json", "yaml", None] = None) -> EBM:
        with open(path, "r") as f:
            if _is_yaml_fmt(path, fmt):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
            return TypeAdapter(cls).validate_python(data)

    def dump(self, path: str, fmt: Literal["json", "yaml", None] = None):
        with open(path, "w") as f:
            if _is_yaml_fmt(path, fmt):
                yaml.safe_dump(json.loads(self.model_dump_json()), f)
            else:
                f.write(self.model_dump_json(indent=2))


@autoregister
class WithTestAndMetricDependencies(EvidentlyBaseModel):
    __type_alias__: ClassVar[Optional[str]] = "evidently:test:WithTestAndMetricDependencies"

    def __evidently_dependencies__(self):
        from evidently.legacy.base_metric import Metric
        from evidently.legacy.tests.base_test import Test

        for field_name, field in itertools.chain(
            self.__dict__.items(), ((pa, getattr(self, pa, None)) for pa in self.__private_attributes__)
        ):
            if issubclass(type(field), (Metric, Test)):
                yield field_name, field


class EnumValueMixin(BaseModel):
    def _to_enum_value(self, key, value):
        field = self.model_fields[key]
        ann = field.annotation
        if isinstance(ann, type) and not issubclass(ann, Enum):
            return value

        if isinstance(value, list):
            return [v.value if isinstance(v, Enum) else v for v in value]

        if isinstance(value, frozenset):
            return frozenset(v.value if isinstance(v, Enum) else v for v in value)

        if isinstance(value, set):
            return {v.value if isinstance(v, Enum) else v for v in value}
        return value.value if isinstance(value, Enum) else value

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        res = super().model_dump(*args, **kwargs)
        return {k: self._to_enum_value(k, v) for k, v in res.items()}

    @model_serializer(mode="wrap")
    def _delegate_serialization(self, nxt: SerializerFunctionWrapHandler, info: SerializationInfo):
        try:
            res = super()._delegate_serialization(nxt, info)
        except AttributeError:
            res = nxt(self)
        return {k: self._to_enum_value(k, v) for k, v in res.items()}


class ExcludeNoneMixin(BaseModel):
    @model_serializer(mode="wrap")
    def _delegate_serialization(self, nxt: SerializerFunctionWrapHandler, info: SerializationInfo):
        try:
            res = super()._delegate_serialization(nxt, info)
        except AttributeError:
            res = nxt(self)
        return {k: v for k, v in res.items() if v is not None}


class FieldTags(Enum):
    Parameter = "parameter"
    Current = "current"
    Reference = "reference"
    Render = "render"
    TypeField = "type_field"
    Extra = "extra"


IncludeTags = FieldTags  # fixme: tmp for compatibility, remove in separate PR


class FieldInfo(EnumValueMixin):
    model_config = ConfigDict(frozen=True)

    path: str
    tags: FrozenSet[FieldTags]
    classpath: str

    def __lt__(self, other):
        return self.path < other.path


def _to_path(path: List[Any]) -> str:
    return ".".join(str(p) for p in path)


class FieldPath:
    def __init__(self, path: List[Any], cls_or_instance: Union[Type, Any], is_mapping: bool = False):
        self._path = path
        self._cls: Type
        self._instance: Any
        if is_union_type(cls_or_instance):
            cls_or_instance = get_args(cls_or_instance)[0]
        if isinstance(cls_or_instance, type):
            self._cls = cls_or_instance
            self._instance = None
        else:
            self._cls = type(cls_or_instance)
            self._instance = cls_or_instance
        self._is_mapping = is_mapping

    @property
    def has_instance(self):
        return self._instance is not None

    def list_fields(self) -> List[str]:
        if self.has_instance and self._is_mapping and isinstance(self._instance, dict):
            return list(self._instance.keys())
        if isinstance(self._cls, type) and issubclass(self._cls, BaseModel):
            return list(self._cls.model_fields)  # type: ignore[call-overload]
        return []

    def __getattr__(self, item) -> "FieldPath":
        return self.child(item)

    def child(self, item: str) -> "FieldPath":
        if self._is_mapping:
            if self.has_instance and isinstance(self._instance, dict):
                return FieldPath(self._path + [item], self._instance[item])
            if not self.has_instance and _is_dict_annotation(self._cls):
                value_type = _get_dict_value_type(self._cls)
                if value_type is not None:
                    return FieldPath(self._path + [item], value_type)
            return FieldPath(self._path + [item], self._cls)
        if not issubclass(self._cls, BaseModel):
            raise AttributeError(f"{self._cls} does not have fields")
        if item not in self._cls.model_fields:  # type: ignore[operator]
            raise AttributeError(f"{self._cls} type does not have '{item}' field")
        field = self._cls.model_fields[item]  # type: ignore[index]
        field_value = get_field_inner_type(field)
        is_mapping = _is_dict_annotation(field.annotation)
        if self.has_instance:
            field_value = getattr(self._instance, item)
            if is_mapping:
                return FieldPath(self._path + [item], field_value, is_mapping=True)
        return FieldPath(self._path + [item], field_value, is_mapping=is_mapping)

    def list_nested_fields(self, exclude: Set["IncludeTags"] = None) -> List[str]:
        if not isinstance(self._cls, type) or not issubclass(self._cls, BaseModel):
            return [repr(self)]
        res = []
        for name, field in self._cls.model_fields.items():  # type: ignore[attr-defined]
            field_value = field.annotation
            # todo: do something with recursive imports
            from evidently.legacy.core import get_field_tags

            field_tags = get_field_tags(self._cls, name)
            if field_tags is not None and (exclude is not None and any(t in exclude for t in field_tags)):
                continue
            is_mapping = _is_dict_annotation(field.annotation)
            if self.has_instance:
                field_value = getattr(self._instance, name)
                if is_mapping and isinstance(field_value, dict):
                    for key, value in field_value.items():
                        res.extend(FieldPath(self._path + [name, str(key)], value).list_nested_fields(exclude=exclude))
                    continue
            else:
                if is_mapping:
                    value_type = _get_dict_value_type(field.annotation)
                    if value_type is not None:
                        res.extend(
                            FieldPath(self._path + [f"{name}.*"], value_type).list_nested_fields(exclude=exclude)
                        )
                    else:
                        res.append(_to_path(self._path + [f"{name}.*"]))
                    continue
            res.extend(FieldPath(self._path + [name], field_value).list_nested_fields(exclude=exclude))
        return res

    def _list_with_tags(self, current_tags: Set["IncludeTags"]) -> List[Tuple[List[Any], Set["IncludeTags"]]]:
        if not isinstance(self._cls, type) or not issubclass(self._cls, BaseModel):
            return [(self._path, current_tags)]
        from evidently.legacy.core import BaseResult

        if issubclass(self._cls, BaseResult) and self._cls.model_config.get("extract_as_obj", False):
            return [(self._path, current_tags)]
        res = []
        from evidently.ui.backport import ByLabelCountValueV1
        from evidently.ui.backport import ByLabelValueV1

        if issubclass(self._cls, ByLabelValueV1):
            res.append((self._path + ["values"], current_tags.union({IncludeTags.Render})))
        if issubclass(self._cls, ByLabelCountValueV1):
            res.append((self._path + ["counts"], current_tags.union({IncludeTags.Render})))
            res.append((self._path + ["shares"], current_tags.union({IncludeTags.Render})))
        for name, field in self._cls.model_fields.items():  # type: ignore[attr-defined]
            field_value = field.annotation

            # todo: do something with recursive imports
            from evidently.legacy.core import get_field_tags

            field_tags = get_field_tags(self._cls, name)

            is_mapping = _is_dict_annotation(field.annotation)
            if self.has_instance:
                field_value = getattr(self._instance, name)
                if is_mapping and isinstance(field_value, dict):
                    for key, value in field_value.items():
                        res.extend(
                            FieldPath(self._path + [name, key], value)._list_with_tags(current_tags.union(field_tags))
                        )
                    continue
            else:
                if is_mapping:
                    name = f"{name}.*"
            res.extend(FieldPath(self._path + [name], field_value)._list_with_tags(current_tags.union(field_tags)))
        return res

    def list_nested_fields_with_tags(self) -> List[Tuple[str, Set["IncludeTags"]]]:
        return [(_to_path(path), tags) for path, tags in self._list_with_tags(set())]

    def list_nested_field_infos(self) -> List[FieldInfo]:
        return [
            FieldInfo(path=_to_path(path), tags=frozenset(tags), classpath=get_classpath(self._get_field_type(path)))
            for path, tags in self._list_with_tags(set())
        ]

    def _get_field_type(self, path: List[str]) -> Type:
        if len(path) == 0:
            raise ValueError("Empty path provided")
        if len(path) == 1:
            if isinstance(self._cls, type) and issubclass(self._cls, BaseModel):
                return self._cls.model_fields[path[0]].annotation  # type: ignore[index]
            if self.has_instance:
                # fixme: tmp fix
                # in case of field like f: Dict[str, A] we wont know that value was type annotated with A when we get to it
                if isinstance(self._instance, dict):
                    return type(self._instance.get(path[0]))
            raise NotImplementedError(f"Not implemented for {self._cls.__name__}")
        child, *path = path
        return self.child(child)._get_field_type(path)

    def __repr__(self):
        return self.get_path()

    def get_path(self):
        return ".".join(self._path)

    def __dir__(self) -> Iterable[str]:
        res: List[str] = []
        res.extend(super().__dir__())
        res.extend(self.list_fields())
        return res

    def get_field_tags(self, path: List[str]) -> Optional[Set["IncludeTags"]]:
        from evidently.legacy.base_metric import BaseResult

        if not isinstance(self._cls, type) or not issubclass(self._cls, BaseResult):
            return None
        self_tags = self._cls.__tags__ or set()
        if len(path) == 0:
            return self_tags
        field_name, *path = path
        # todo: do something with recursive imports
        from evidently.legacy.core import get_field_tags

        field_tags = get_field_tags(self._cls, field_name)
        return self_tags.union(field_tags).union(self.child(field_name).get_field_tags(path) or tuple())


@pydantic_type_validator(FieldPath)
def field_path_validator(value):
    return value.get_path()


def get_object_hash_deprecated(obj: Union[BaseModel, dict]):
    from evidently.legacy.utils import NumpyEncoder

    if isinstance(obj, BaseModel):
        obj = obj.model_dump()
    return hashlib.md5(json.dumps(obj, cls=NumpyEncoder).encode("utf8"), **md5_kwargs).hexdigest()  # nosec: B324


class AutoAliasMixin:
    __alias_type__: ClassVar[str]
    __type_alias__: ClassVar[Optional[str]] = None

    @classmethod
    def __get_type__(cls) -> str:
        type_alias = cls.__dict__.get("__type_alias__")
        if type_alias is not None:
            return str(type_alias)
        if not hasattr(cls, "__alias_type__"):
            raise TypeError(f"{cls.__name__} `__alias_type__` is not defined")
        return f"evidently:{cls.__alias_type__}:{cls.__name__}"


def get_field_inner_type(field: PydanticFieldInfo) -> Type:
    """Return the inner type of a Pydantic field, unwrapping containers like Optional, List, etc."""
    typ = field.annotation
    while True:
        origin = get_origin(typ)
        args = get_args(typ)
        # Unwrap Annotated
        if origin is Annotated:
            typ = args[0]
            continue
        # Unwrap Optional/Union[T, None]
        if origin is Union:
            non_none = [t for t in args if t is not type(None)]
            if len(non_none) == 1:
                typ = non_none[0]
                continue
        # Unwrap list, set, tuple, etc.
        if origin in (list, set, tuple):
            if args:
                typ = args[0]
                continue
        if origin is dict:
            typ = args[1]
            break
        break
    if typ is None:
        raise TypeError(f"Field {field} does not have correct type annotation ")
    return typ


def get_field_outer_type(field: PydanticFieldInfo) -> Type:
    typ = field.annotation
    if get_origin(typ) is Union:
        args = get_args(typ)
        if len(args) == 2 and type(None) in args:
            typ = [a for a in args if a is not type(None)][0]
    if typ is None:
        raise TypeError(f"Field {field} does not have correct type annotation")
    return typ


def force_keys_to_str(value: Optional[dict[Any, Any]]) -> Optional[dict[str, Any]]:
    if value is None:
        return None
    return {str(k): v for k, v in value.items()}


StrKeyValidator = BeforeValidator(force_keys_to_str)
