import abc
import logging
from copy import copy
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

from evidently.features.generated_features import GeneratedFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr
    from pydantic.typing import DictStrAny
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


class MetricResultField(BaseModel):
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

    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        include = include or self.__config__.dict_include_fields or set(self.__fields__)
        exclude = copy(exclude) or self.__config__.dict_exclude_fields or set()

        for name, field in self.__fields__.items():
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResultField):
                if not field.type_.__config__.dict_include:
                    if isinstance(exclude, set):
                        exclude.add(name)
                    elif isinstance(exclude, dict):
                        exclude[name] = True
                    else:
                        raise ValueError("Unknown exclude value type")
        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def collect_pandas_columns(self, prefix="", include: Set[str] = None, exclude: Set[str] = None) -> Dict[str, Any]:
        include = include or self.__config__.pd_include_fields or set(self.__fields__)
        exclude = exclude or self.__config__.pd_exclude_fields or set()

        data = {}
        for name, field in self.__fields__.items():
            if name not in include or name in exclude:
                continue
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResultField):
                if field.type_.__config__.pd_include:
                    field_value = getattr(self, name)
                    field_prefix = f"{prefix}{self.__config__.pd_name_mapping.get(name, name)}_"
                    if field_value is None:
                        continue
                    elif isinstance(field_value, MetricResultField):
                        data.update(field_value.collect_pandas_columns(field_prefix))
                    elif isinstance(field_value, dict):  # Dict[str, MetricResultField]
                        # todo: deal with more complex stuff later
                        assert all(isinstance(v, MetricResultField) for v in field_value.values())
                        dict_value: MetricResultField
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


class MetricResult(MetricResultField):
    def get_dict(self):
        if not self.__config__.dict_include:
            return {}
        exclude = set(self.__config__.dict_exclude_fields)
        for name, field in self.__fields__.items():
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResultField):
                if not field.type_.__config__.dict_include:
                    exclude.add(name)
        return self.dict(include=self.__config__.dict_include_fields or None, exclude=exclude)


class ColumnMetricResult(MetricResult):
    column_name: str
    # todo: use enum
    column_type: str

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict({self.column_name: self.collect_pandas_columns()}, orient="index")


ColumnTResult = TypeVar("ColumnTResult", bound=ColumnMetricResult)


class ColumnMetric(Metric, Generic[ColumnTResult], abc.ABC):
    column_name: str
