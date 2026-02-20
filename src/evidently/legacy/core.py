import uuid
from enum import Enum
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast
from typing import get_args
from typing import get_origin

import numpy as np
import pandas as pd
import uuid6
from pydantic import BaseModel
from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic.fields import FieldInfo
from typing_inspect import is_literal_type

from evidently.pydantic_utils import IncludeTags
from evidently.pydantic_utils import get_field_inner_type
from evidently.pydantic_utils import pydantic_type_validator

if TYPE_CHECKING:
    from typing import AbstractSet
    from typing import Mapping as MappingIntStrAny

    AbstractSetIntStr = AbstractSet[Union[int, str]]

IncludeOptions = Union["AbstractSetIntStr", "MappingIntStrAny"]


Label = Union[int, str, float, None]


def try_int_validator(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


LabelIntStr = Annotated[Label, BeforeValidator(try_int_validator)]


class ColumnType(Enum):
    """Column data type enumeration.

    Represents the type of data in a column. Used for automatic type inference
    and to determine which metrics and tests are applicable.
    """

    Numerical = "num"
    """Numeric columns (integers, floats)."""
    Categorical = "cat"
    """Categorical columns with limited distinct values."""
    Text = "text"
    """Text/string columns."""
    Datetime = "datetime"
    """DateTime columns."""
    Date = "data"
    """Date columns."""
    Id = "id"
    """Identifier columns."""
    Unknown = "unknown"
    """Columns with unknown or unclassified type."""
    List = "list"
    """Columns containing lists or arrays."""


def _strip_union(type_):
    if get_origin(type_) is Union:
        args = [a for a in get_args(type_) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return type_


def _is_mapping_field(field: FieldInfo):
    return get_origin(_strip_union(field.annotation)) is dict


def _is_sequence_field(field: FieldInfo):
    return get_origin(_strip_union(field.annotation)) in (list, set, tuple)


@pydantic_type_validator(pd.Series)
def series_validator(value):
    return pd.Series(value)


@pydantic_type_validator(pd.DataFrame)
def dataframe_validator(value):
    return pd.DataFrame(value)


# @pydantic_type_validator(pd.Index)
# def index_validator(value):
#     return pd.Index(value)


# @pydantic_type_validator(np.double)
# def np_inf_valudator(value):
#     return np.float(value)


def np_inf_validator(value):
    return float(value) if value is not None else None


PydanticNPDouble = Annotated[np.double, BeforeValidator(np_inf_validator)]

# @pydantic_type_validator(np.ndarray)
# def np_array_valudator(value):
#     return np.array(value)


def np_array_validator(value):
    return np.array(value)


PydanticNPArray = Annotated[np.ndarray, BeforeValidator(np_array_validator)]


class BaseResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    __dict_include__: ClassVar[bool] = True
    __pd_include__: ClassVar[bool] = True
    __pd_name_mapping__: ClassVar[Optional[Dict[str, str]]] = None

    __dict_include_fields__: ClassVar[Optional[set]] = None
    __dict_exclude_fields__: ClassVar[Optional[set]] = None
    __pd_include_fields__: ClassVar[Optional[set]] = None
    __pd_exclude_fields__: ClassVar[Optional[set]] = None

    __tags__: ClassVar[Optional[Set[IncludeTags]]] = None
    __field_tags__: ClassVar[Optional[Dict[str, set]]] = None
    __extract_as_obj__: ClassVar[bool] = False

    def get_dict(
        self,
        include_render: bool = False,
        include: Optional[IncludeOptions] = None,
        exclude: Optional[IncludeOptions] = None,
    ):
        exclude_tags = {IncludeTags.TypeField}
        if not include_render:
            exclude_tags.add(IncludeTags.Render)
        dump_include = include or self._build_include(exclude_tags=exclude_tags)
        dump_exclude = exclude
        return self.model_dump(
            include=cast(Optional[Union[Set[int], Set[str], Dict[str, Any], Dict[int, Any]]], dump_include),
            exclude=cast(Optional[Union[Set[int], Set[str], Dict[str, Any], Dict[int, Any]]], dump_exclude),
        )

    def _build_include(
        self,
        exclude_tags: Set[IncludeTags],
        include=None,
    ) -> "MappingIntStrAny":
        cls = type(self)
        if not cls.__dict_include__ and not include or any(t in exclude_tags for t in (cls.__tags__ or set())):
            return {}
        include = include or {}
        dict_include_fields = set(() if isinstance(include, bool) else include) or (
            cls.__dict_include_fields__ or set(self.model_fields.keys())
        )
        dict_exclude_fields = cls.__dict_exclude_fields__ or set()
        field_tags = get_all_fields_tags(self.__class__)
        result: Dict[str, Any] = {}
        for name, field in self.model_fields.items():
            if field_tags.get(name) and any(tag in exclude_tags for tag in field_tags.get(name, set())):
                continue
            inner_type = get_field_inner_type(field)
            if isinstance(inner_type, type) and issubclass(inner_type, BaseResult):
                if (
                    (not inner_type.__dict_include__ or name in dict_exclude_fields)
                    and not getattr(field, "include", None)
                    and name not in include
                ):
                    continue

                field_value = getattr(self, name)
                if field_value is None:
                    build_include = {}
                elif _is_mapping_field(field):
                    build_include = {
                        k: v._build_include(exclude_tags=exclude_tags, include=include.get(name, {}))
                        for k, v in field_value.items()
                    }
                elif _is_sequence_field(field):
                    build_include = {
                        i: v._build_include(exclude_tags=exclude_tags, include=include.get(name, {}))
                        for i, v in enumerate(field_value)
                    }
                else:
                    build_include = field_value._build_include(exclude_tags=exclude_tags, include=include.get(name, {}))
                result[name] = build_include
                continue
            if name in dict_exclude_fields and name not in include:
                continue
            if name not in dict_include_fields:
                continue
            result[name] = True
        return result  # type: ignore

    def __init_subclass__(cls, **kwargs):
        cls.__include_fields__ = None

    def collect_pandas_columns(self, prefix="", include: Set[str] = None, exclude: Set[str] = None) -> Dict[str, Any]:
        cls = type(self)
        include = include or cls.__pd_include_fields__ or set(self.model_fields)
        exclude = exclude or cls.__pd_exclude_fields__ or set()

        data = {}
        field_tags = cls.__field_tags__ or {}
        for name, field in self.model_fields.items():
            if field_tags.get(name) and any(
                ft in {IncludeTags.TypeField, IncludeTags.Render} for ft in field_tags.get(name, set())
            ):
                continue
            if name not in include or name in exclude:
                continue
            field_value = getattr(self, name)
            field_prefix = f"{prefix}{(cls.__pd_name_mapping__ or {}).get(name, name)}_"
            if isinstance(field_value, BaseResult):
                field_type = type(field_value)
                if field_type.__pd_include__:
                    if field_value is None:
                        continue
                    if isinstance(field_value, BaseResult):
                        data.update(field_value.collect_pandas_columns(field_prefix))
                continue
            if isinstance(field_value, dict):
                # todo: deal with more complex stuff later
                if all(isinstance(v, BaseResult) for v in field_value.values()):
                    raise NotImplementedError(
                        f"{self.__class__.__name__} does not support dataframe rendering. Please submit an issue to https://github.com/evidentlyai/evidently/issues"
                    )
                dict_value: BaseResult
                for dict_key, dict_value in field_value.items():
                    for (
                        key,
                        value,
                    ) in dict_value.collect_pandas_columns().items():
                        data[f"{field_prefix}_{dict_key}_{key}"] = value
                continue
            data[prefix + name] = field_value
        return data

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame([self.collect_pandas_columns()])


T = TypeVar("T")


def _get_actual_type(cls: Type[T]) -> Type[T]:
    if isinstance(cls, type):
        return cls
    if cls is Any:
        return type
    if is_literal_type(cls):
        return _get_actual_type(type(get_args(cls)[0]))
    return _get_actual_type(get_args(cls)[0])


def _iterate_base_result_types(cls: Type[BaseModel]) -> Iterator[Type[BaseResult]]:
    for type_ in cls.__mro__:
        if not issubclass(type_, BaseResult):
            return
        yield type_


def get_cls_tags(cls: Type[BaseModel]) -> Set[IncludeTags]:
    if issubclass(cls, BaseResult):
        return cls.__tags__ or set()
    return set()


def get_field_tags(cls: Type[BaseModel], field_name: str) -> Set[IncludeTags]:
    field_tags = set()
    for type_ in _iterate_base_result_types(cls):
        ft = type_.__field_tags__ or {}
        if field_name not in ft:
            continue
        field_tags = ft[field_name]
        break

    field = cls.model_fields[field_name]  # type: ignore[index]
    field_annotation = field.annotation
    if field_annotation is None:
        field_annotation = type(None)
    field_type = _get_actual_type(field_annotation)
    self_tags = set() if not issubclass(cls, BaseResult) else (cls.__tags__ or set())
    cls_tags = get_cls_tags(field_type)
    return self_tags.union(field_tags).union(cls_tags)


def get_all_fields_tags(cls: Type[BaseResult]) -> Dict[str, Set[IncludeTags]]:
    return {field_name: get_field_tags(cls, field_name) for field_name in cls.model_fields}  # type: ignore[attr-defined]


def new_id() -> uuid.UUID:
    return uuid6.uuid7()
