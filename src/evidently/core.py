from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Set
from typing import Type
from typing import Union

import numpy as np
import pandas as pd

from evidently._pydantic_compat import SHAPE_DICT
from evidently._pydantic_compat import SHAPE_LIST
from evidently._pydantic_compat import SHAPE_SET
from evidently._pydantic_compat import SHAPE_TUPLE
from evidently._pydantic_compat import ModelField
from evidently.pydantic_utils import pydantic_type_validator

if TYPE_CHECKING:
    from evidently._pydantic_compat import MappingIntStrAny, AbstractSetIntStr

from enum import Enum

from evidently._pydantic_compat import BaseConfig
from evidently._pydantic_compat import BaseModel

IncludeOptions = Union["AbstractSetIntStr", "MappingIntStrAny"]


class ColumnType(Enum):
    Numerical = "num"
    Categorical = "cat"
    Text = "text"
    Datetime = "datetime"
    Date = "data"
    Id = "id"
    Unknown = "unknown"


def _is_mapping_field(field: ModelField):
    return field.shape in (SHAPE_DICT,)


def _is_sequence_field(field: ModelField):
    return field.shape in (SHAPE_LIST, SHAPE_SET, SHAPE_TUPLE)


# workaround for https://github.com/pydantic/pydantic/issues/5301
class AllDict(dict):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def __contains__(self, item):
        return True

    def get(self, __key):
        return self._value

    def __repr__(self):
        return f"{{'__all__':{self._value}}}"

    def __bool__(self):
        return True


class IncludeTags(Enum):
    Render = "render"
    TypeField = "type_field"


@pydantic_type_validator(pd.Series)
def series_validator(value):
    return pd.Series(value)


@pydantic_type_validator(pd.DataFrame)
def dataframe_validator(value):
    return pd.DataFrame(value)


# @pydantic_type_validator(pd.Index)
# def index_validator(value):
#     return pd.Index(value)


@pydantic_type_validator(np.float_)
def np_inf_valudator(value):
    return np.float(value)


@pydantic_type_validator(np.ndarray)
def np_array_valudator(value):
    return np.array(value)


class BaseResult(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        dict_include: bool = True
        pd_include: bool = True
        pd_name_mapping: Dict[str, str] = {}

        dict_include_fields: set = set()
        dict_exclude_fields: set = set()
        pd_include_fields: set = set()
        pd_exclude_fields: set = set()

        tags: Set[IncludeTags] = set()
        field_tags: Dict[str, set] = {}

    if TYPE_CHECKING:
        __config__: ClassVar[Type[Config]] = Config

    def get_dict(
        self,
        include_render: bool = False,
        include: Optional[IncludeOptions] = None,
        exclude: Optional[IncludeOptions] = None,
    ):
        include_tags = set()
        if include_render:
            include_tags.add(IncludeTags.Render)
        return self.dict(include=include or self._build_include(include_tags=include_tags), exclude=exclude)

    def _build_include(
        self,
        include_tags: Set[IncludeTags],
        include=None,
    ) -> "MappingIntStrAny":
        if (
            not self.__config__.dict_include
            and not include
            and all(t not in include_tags for t in self.__config__.tags)
        ):
            return {}
        include = include or {}
        dict_include_fields = (
            set(() if isinstance(include, bool) else include)
            or self.__config__.dict_include_fields
            or set(self.__fields__.keys())
        )
        dict_exclude_fields = self.__config__.dict_exclude_fields or set()
        field_tags = self.__config__.field_tags or {}
        result: Dict[str, Any] = {}
        for name, field in self.__fields__.items():
            if field_tags.get(name) and all(tag not in include_tags for tag in field_tags.get(name, set())):
                continue
            if isinstance(field.type_, type) and issubclass(field.type_, BaseResult):
                if (
                    (not field.type_.__config__.dict_include or name in dict_exclude_fields)
                    and not field.field_info.include
                    and name not in include
                    and all(tag not in include_tags for tag in field.type_.__config__.tags)
                ):
                    continue

                field_value = getattr(self, name)
                if field_value is None:
                    build_include = {}
                elif _is_mapping_field(field):
                    build_include = {
                        k: v._build_include(
                            include_tags=include_tags, include=field.field_info.include or include.get(name, {})
                        )
                        for k, v in field_value.items()
                    }
                elif _is_sequence_field(field):
                    build_include = {
                        i: v._build_include(
                            include_tags=include_tags, include=field.field_info.include or include.get(name, {})
                        )
                        for i, v in enumerate(field_value)
                    }
                else:
                    build_include = field_value._build_include(
                        include_tags=include_tags, include=field.field_info.include or include.get(name, {})
                    )
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
        include = include or self.__config__.pd_include_fields or set(self.__fields__)
        exclude = exclude or self.__config__.pd_exclude_fields or set()

        data = {}
        for name, field in self.__fields__.items():
            if name not in include or name in exclude:
                continue
            if isinstance(field.type_, type) and issubclass(field.type_, BaseResult):
                if field.type_.__config__.pd_include:
                    field_value = getattr(self, name)
                    field_prefix = f"{prefix}{self.__config__.pd_name_mapping.get(name, name)}_"
                    if field_value is None:
                        continue
                    elif isinstance(field_value, BaseResult):
                        data.update(field_value.collect_pandas_columns(field_prefix))
                    elif isinstance(field_value, dict):  # Dict[str, MetricResultField]
                        # todo: deal with more complex stuff later
                        assert all(isinstance(v, BaseResult) for v in field_value.values())
                        dict_value: BaseResult
                        for dict_key, dict_value in field_value.items():
                            for (
                                key,
                                value,
                            ) in dict_value.collect_pandas_columns().items():
                                data[f"{field_prefix}_{dict_key}_{key}"] = value
                    elif isinstance(field_value, list):  # List[MetricResultField]
                        raise NotImplementedError  # todo
                continue
            data[prefix + name] = getattr(self, name)
        return data

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame([self.collect_pandas_columns()])
