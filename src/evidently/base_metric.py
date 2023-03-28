import abc
import logging
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd
from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic.fields import SHAPE_DICT
from pydantic.fields import ModelField

from evidently.features.generated_features import GeneratedFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr
    from pydantic.typing import MappingIntStrAny

TResult = TypeVar("TResult", bound="MetricResult")


class ErrorResult:
    exception: BaseException

    def __init__(self, exception: BaseException):
        self.exception = exception


class DatasetType(Enum):
    MAIN = "main"
    ADDITIONAL = "additional"


@dataclass(eq=True, unsafe_hash=True)
class ColumnName:
    name: str
    display_name: str
    dataset: DatasetType
    feature_class: Optional[GeneratedFeature]

    def is_main_dataset(self):
        return self.dataset == DatasetType.MAIN

    @staticmethod
    def main_dataset(name: str):
        return ColumnName(name, name, DatasetType.MAIN, None)


def additional_feature(feature: GeneratedFeature, feature_name: str, display_name: str) -> ColumnName:
    return ColumnName(
        name=feature.__class__.__name__ + "." + feature_name,
        display_name=display_name,
        dataset=DatasetType.ADDITIONAL,
        feature_class=feature,
    )


class ColumnNotFound(BaseException):
    def __init__(self, column_name: str):
        self.column_name = column_name


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    reference_additional_features: Optional[pd.DataFrame]
    current_additional_features: Optional[pd.DataFrame]
    column_mapping: ColumnMapping
    data_definition: DataDefinition

    @staticmethod
    def _get_by_column_name(dataset: pd.DataFrame, additional: pd.DataFrame, column: ColumnName) -> pd.Series:
        if column.dataset == DatasetType.MAIN:
            if column.name not in dataset.columns:
                raise ColumnNotFound(column.name)
            return dataset[column.name]
        if column.dataset == DatasetType.ADDITIONAL:
            return additional[column.name]
        raise ValueError("unknown column data")

    def get_current_column(self, column: Union[str, ColumnName]) -> pd.Series:
        if isinstance(column, str):
            _column = ColumnName(column, column, DatasetType.MAIN, None)
        else:
            _column = column
        return self._get_by_column_name(self.current_data, self.current_additional_features, _column)

    def get_reference_column(self, column: Union[str, ColumnName]) -> Optional[pd.Series]:
        if self.reference_data is None:
            return None
        if isinstance(column, str):
            _column = ColumnName(column, column, DatasetType.MAIN, None)
        else:
            _column = column
        if self.reference_additional_features is None and _column.dataset == DatasetType.ADDITIONAL:
            return None
        return self._get_by_column_name(self.reference_data, self.reference_additional_features, _column)


class Metric(Generic[TResult]):
    context = None

    def get_id(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def calculate(self, data: InputData) -> TResult:
        raise NotImplementedError()

    def set_context(self, context):
        self.context = context

    def get_result(self) -> TResult:
        if self.context is None:
            raise ValueError("No context is set")
        result = self.context.metric_results.get(self, None)
        if isinstance(result, ErrorResult):
            raise result.exception
        if result is None:
            raise ValueError(f"No result found for metric {self} of type {type(self).__name__}")
        return result

    def get_parameters(self) -> Optional[tuple]:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if isinstance(value, list):
                attributes.append(tuple(value))
            else:
                attributes.append(value)
        params = tuple(attributes)
        try:
            hash(params)
        except TypeError:
            logging.warning(f"unhashable params for {type(self)}. Fallback to unique.")
            return None
        return params

    def required_features(self, data_definition: DataDefinition) -> List[GeneratedFeature]:
        required_features = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if issubclass(type(value), ColumnName) and value.feature_class is not None:
                required_features.append(value.feature_class)
        return required_features


def _is_mapping_field(field: ModelField):
    return field.shape in (SHAPE_DICT,)


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


class MetricResult(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        dict_include: bool = True
        pd_include: bool = True
        pd_name_mapping: Dict[str, str] = {}

        dict_include_fields: set = set()
        dict_exclude_fields: set = set()
        pd_include_fields: set = set()
        pd_exclude_fields: set = set()

    if TYPE_CHECKING:
        __config__: ClassVar[Type[Config]] = Config

    def get_dict(
        self,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
    ):
        return self.dict(include=include or self._build_include(), exclude=exclude)

    def _build_include(self, include=None) -> "MappingIntStrAny":
        if not self.__config__.dict_include and not include:
            return {}
        include = include or {}
        dict_include_fields = (
            set(() if isinstance(include, bool) else include)
            or self.__config__.dict_include_fields
            or set(self.__fields__.keys())
        )
        dict_exclude_fields = self.__config__.dict_exclude_fields or set()
        result: Dict[str, Any] = {}
        for name, field in self.__fields__.items():
            if name in dict_exclude_fields and name not in include:
                continue
            if name not in dict_include_fields:
                continue
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResult):
                if field.type_.__config__.dict_include or field.field_info.include or name in include:
                    field_value = getattr(self, name)
                    if field_value is None:
                        build_include = {}
                    elif _is_mapping_field(field):
                        build_include = {
                            k: v._build_include(include=field.field_info.include or include.get(name, {}))
                            for k, v in field_value.items()
                        }
                    # todo: lists

                    else:
                        build_include = field_value._build_include(
                            include=field.field_info.include or include.get(name, {})
                        )
                    result[name] = build_include
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
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResult):
                if field.type_.__config__.pd_include:
                    field_value = getattr(self, name)
                    field_prefix = f"{prefix}{self.__config__.pd_name_mapping.get(name, name)}_"
                    if field_value is None:
                        continue
                    elif isinstance(field_value, MetricResult):
                        data.update(field_value.collect_pandas_columns(field_prefix))
                    elif isinstance(field_value, dict):  # Dict[str, MetricResultField]
                        # todo: deal with more complex stuff later
                        assert all(isinstance(v, MetricResult) for v in field_value.values())
                        dict_value: MetricResult
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


class ColumnMetricResult(MetricResult):
    column_name: str
    # todo: use enum
    column_type: str

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict({self.column_name: self.collect_pandas_columns()}, orient="index")


ColumnTResult = TypeVar("ColumnTResult", bound=ColumnMetricResult)


class ColumnMetric(Metric, Generic[ColumnTResult], abc.ABC):
    column_name: str
