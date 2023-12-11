import abc
import logging
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd

from evidently._pydantic_compat import ModelMetaclass
from evidently.core import BaseResult
from evidently.core import ColumnType
from evidently.core import IncludeTags
from evidently.features.generated_features import GeneratedFeature
from evidently.options.base import AnyOptions
from evidently.options.base import Options
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import FieldPath
from evidently.pydantic_utils import FrozenBaseMeta
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import WithTestAndMetricDependencies
from evidently.utils.data_preprocessing import DataDefinition

if TYPE_CHECKING:
    from evidently.suite.base_suite import Context


class WithFieldsPathMetaclass(ModelMetaclass):
    @property
    def fields(cls) -> FieldPath:
        return FieldPath([], cls)


class MetricResult(PolymorphicModel, BaseResult, metaclass=WithFieldsPathMetaclass):  # type: ignore[misc] # pydantic Config
    class Config:
        field_tags = {"type": {IncludeTags.TypeField}}


class ErrorResult(BaseResult):
    class Config:
        underscore_attrs_are_private = True

    _exception: Optional[BaseException] = None  # todo: fix serialization of exceptions

    def __init__(self, exception: Optional[BaseException]):
        super().__init__()
        self._exception = exception

    @property
    def exception(self):
        return self._exception


class DatasetType(Enum):
    MAIN = "main"
    ADDITIONAL = "additional"


class ColumnName(EnumValueMixin, EvidentlyBaseModel):
    name: str
    display_name: str
    dataset: DatasetType
    feature_class: Optional[GeneratedFeature]

    def __init__(
        self, name: str, display_name: str, dataset: DatasetType, feature_class: Optional[GeneratedFeature] = None
    ):
        super().__init__(name=name, display_name=display_name, dataset=dataset, feature_class=feature_class)

    def is_main_dataset(self):
        return self.dataset == DatasetType.MAIN

    @staticmethod
    def main_dataset(name: str):
        return ColumnName(name, name, DatasetType.MAIN, None)

    def __str__(self):
        return self.display_name

    @classmethod
    def from_any(cls, column_name: Union[str, "ColumnName"]):
        return column_name if not isinstance(column_name, str) else ColumnName.main_dataset(column_name)


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
class GenericInputData:
    reference_data: Optional[object]
    current_data: object
    column_mapping: ColumnMapping
    data_definition: DataDefinition
    additional_data: Dict[str, Any]


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    reference_additional_features: Optional[pd.DataFrame]
    current_additional_features: Optional[pd.DataFrame]
    column_mapping: ColumnMapping
    data_definition: DataDefinition
    additional_data: Dict[str, Any]

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
        _column = self._str_to_column_name(column)
        return self._get_by_column_name(self.current_data, self.current_additional_features, _column)

    def get_reference_column(self, column: Union[str, ColumnName]) -> Optional[pd.Series]:
        if self.reference_data is None:
            return None
        _column = self._str_to_column_name(column)
        if self.reference_additional_features is None and _column.dataset == DatasetType.ADDITIONAL:
            return None
        return self._get_by_column_name(self.reference_data, self.reference_additional_features, _column)

    def get_data(self, column: Union[str, ColumnName]) -> Tuple[ColumnType, pd.Series, Optional[pd.Series]]:
        ref_data = None
        if self.reference_data is not None:
            ref_data = self.get_reference_column(column)
        return self._determine_type(column), self.get_current_column(column), ref_data

    def _determine_type(self, column: Union[str, ColumnName]) -> ColumnType:
        if isinstance(column, ColumnName) and column.feature_class is not None:
            column_type = ColumnType.Numerical
        else:
            if isinstance(column, ColumnName):
                column_name = column.name
            else:
                column_name = column
            column_type = self.data_definition.get_column(column_name).column_type
        return column_type

    def has_column(self, column_name: Union[str, ColumnName]):
        column = self._str_to_column_name(column_name)
        if column.dataset == DatasetType.MAIN:
            return column.name in [definition.column_name for definition in self.data_definition.get_columns()]
        if self.current_additional_features is not None:
            return column.name in self.current_additional_features.columns
        return False

    def _str_to_column_name(self, column: Union[str, ColumnName]) -> ColumnName:
        if isinstance(column, str):
            _column = ColumnName(column, column, DatasetType.MAIN, None)
        else:
            _column = column
        return _column


TResult = TypeVar("TResult", bound=MetricResult)


class WithResultFieldPathMetaclass(FrozenBaseMeta):
    def result_type(cls) -> Type[MetricResult]:
        return cls.__orig_bases__[0].__args__[0]  # type: ignore[attr-defined]

    @property
    def fields(cls) -> FieldPath:
        return FieldPath([], cls.result_type())


class Metric(WithTestAndMetricDependencies, Generic[TResult], metaclass=WithResultFieldPathMetaclass):
    _context: Optional["Context"] = None

    # TODO: if we want metric-specific options
    options: Options

    # resulting options will be determined via
    # options = global_option.override(display_options).override(metric_options)

    def __init__(self, options: AnyOptions = None, **data):
        self.options = Options.from_any_options(options)
        super().__init__(**data)

    def get_id(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def calculate(self, data: InputData) -> TResult:
        raise NotImplementedError()

    def set_context(self, context):
        self._context = context

    def get_result(self) -> TResult:
        if not hasattr(self, "_context") or self._context is None:
            raise ValueError("No context is set")
        result = self._context.metric_results.get(self, None)
        if isinstance(result, ErrorResult):
            raise result.exception
        if result is None:
            raise ValueError(f"No result found for metric {self} of type {type(self).__name__}")
        return result  # type: ignore[return-value]

    def get_parameters(self) -> Optional[tuple]:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["_context"]:
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

    def get_options(self):
        options = self.options if hasattr(self, "options") else Options()
        if self._context is not None:
            options = self._context.options.override(options)
        return options


class ColumnMetricResult(MetricResult):
    column_name: str
    # todo: use enum
    column_type: str

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict({self.column_name: self.collect_pandas_columns()}, orient="index")


ColumnTResult = TypeVar("ColumnTResult", bound=ColumnMetricResult)


class ColumnMetric(Metric[ColumnTResult], Generic[ColumnTResult], abc.ABC):
    column_name: ColumnName

    def __init__(self, column_name: Union[ColumnName, str], options: AnyOptions = None):
        self.column_name = ColumnName.from_any(column_name)
        super().__init__(options)
