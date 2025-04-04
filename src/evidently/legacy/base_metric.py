import abc
import logging
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd
import typing_inspect

from evidently._pydantic_compat import Field
from evidently._pydantic_compat import ModelMetaclass
from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.core import BaseResult
from evidently.legacy.core import ColumnType
from evidently.legacy.core import IncludeTags
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import FieldPath
from evidently.pydantic_utils import FingerprintPart
from evidently.pydantic_utils import FrozenBaseMeta
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import WithTestAndMetricDependencies
from evidently.pydantic_utils import autoregister
from evidently.pydantic_utils import get_value_fingerprint

if TYPE_CHECKING:
    from evidently.legacy.features.generated_features import GeneratedFeatures
    from evidently.legacy.suite.base_suite import Context


class WithFieldsPathMetaclass(ModelMetaclass):
    @property
    def fields(cls) -> FieldPath:
        return FieldPath([], cls)


class MetricResult(PolymorphicModel, BaseResult, metaclass=WithFieldsPathMetaclass):  # type: ignore[misc] # pydantic Config
    class Config:
        type_alias = "evidently:metric_result:MetricResult"
        field_tags = {"type": {IncludeTags.TypeField}}
        is_base_type = True
        alias_required = True


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


DisplayName = str


@autoregister
class ColumnName(EnumValueMixin, EvidentlyBaseModel):
    class Config:
        type_alias = "evidently:base:ColumnName"

    name: str
    display_name: DisplayName
    dataset: DatasetType
    _feature_class: Optional["GeneratedFeatures"] = PrivateAttr(None)

    def __init__(
        self, name: str, display_name: str, dataset: DatasetType, feature_class: Optional["GeneratedFeatures"] = None
    ):
        self._feature_class = feature_class
        super().__init__(name=name, display_name=display_name, dataset=dataset)

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

    @property
    def feature_class(self) -> Optional["GeneratedFeatures"]:
        return self._feature_class

    def get_fingerprint_parts(self) -> Tuple[FingerprintPart, ...]:
        return tuple(
            (name, self.get_field_fingerprint(name))
            for name, field in sorted(self.__fields__.items())
            if field.required or getattr(self, name) != field.get_default() and field.name != "display_name"
        )


class ColumnNotFound(BaseException):
    def __init__(self, column_name: str):
        self.column_name = column_name


TEngineDataType = TypeVar("TEngineDataType")


@dataclass
class GenericInputData(Generic[TEngineDataType]):
    reference_data: Optional[TEngineDataType]
    current_data: TEngineDataType
    column_mapping: ColumnMapping
    data_definition: DataDefinition
    additional_data: Dict[str, Any]
    reference_additional_features: Optional[TEngineDataType] = None
    current_additional_features: Optional[TEngineDataType] = None

    def get_datasets(self) -> Tuple[Optional[TEngineDataType], TEngineDataType]:
        raise NotImplementedError


class InputData(GenericInputData[pd.DataFrame]):
    @staticmethod
    def _get_by_column_name(dataset: pd.DataFrame, additional: Optional[pd.DataFrame], column: ColumnName) -> pd.Series:
        if column.dataset == DatasetType.MAIN:
            if column.name not in dataset.columns:
                raise ColumnNotFound(column.name)
            return dataset[column.name]
        if column.dataset == DatasetType.ADDITIONAL:
            if additional is None:
                raise ValueError("no additional dataset is provided, but field requested")
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
            column_type = column.feature_class.get_type(column.name)
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

    def get_datasets(self) -> Tuple[Optional[pd.DataFrame], pd.DataFrame]:
        current = self.current_data
        if self.current_additional_features is not None:
            current = self.current_data.join(self.current_additional_features)
        reference = self.reference_data
        if self.reference_data is not None and self.reference_additional_features is not None:
            reference = self.reference_data.join(self.reference_additional_features)
        return reference, current


TResult = TypeVar("TResult", bound=MetricResult)


class FieldsDescriptor:
    def __get__(self, instance: Optional["Metric"], type: Type["Metric"]) -> FieldPath:
        if instance is not None:
            try:
                return FieldPath([], instance.get_result())
            except ValueError:
                warnings.warn("Metric is not calculated yet, using generic fields list")
        return FieldPath([], type.result_type())


class WithResultFieldPathMetaclass(FrozenBaseMeta):
    def result_type(cls) -> Type[MetricResult]:
        return typing_inspect.get_args(
            next(b for b in cls.__orig_bases__ if typing_inspect.is_generic_type(b))  # type: ignore[attr-defined]
        )[0]


class BasePreset(EvidentlyBaseModel):
    class Config:
        type_alias = "evidently:base:BasePreset"
        transitive_aliases = True
        is_base_type = True


class Metric(WithTestAndMetricDependencies, Generic[TResult], metaclass=WithResultFieldPathMetaclass):
    class Config:
        is_base_type = True

    _context: Optional["Context"] = None

    options: Optional[Options] = Field(default=None)

    fields: ClassVar[FieldsDescriptor] = FieldsDescriptor()
    # resulting options will be determined via
    # options = global_option.override(display_options).override(metric_options)

    def __init__(self, options: AnyOptions = None, **data):
        self.options = Options.from_any_options(options)
        super().__init__(**data)

    @classmethod
    def get_id(cls) -> str:
        return cls.__name__

    @classmethod
    def get_group(cls) -> str:
        if cls.__module__.startswith("evidently.legacy.metrics."):
            return cls.__module__.split(".")[2]
        return ""

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

    def required_features(self, data_definition: DataDefinition) -> List["GeneratedFeatures"]:
        required_features = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if isinstance(value, ColumnName) and value.feature_class is not None:
                required_features.append(value.feature_class)
        return required_features

    def get_options(self):
        options = self.options if hasattr(self, "options") else Options()
        if self._context is not None:
            options = self._context.options.override(options)
        return options

    def get_field_fingerprint(self, field: str) -> FingerprintPart:
        if field == "options":
            return self.get_options_fingerprint()
        return super().get_field_fingerprint(field)

    def get_options_fingerprint(self) -> FingerprintPart:
        return None


class UsesRawDataMixin:
    options: Options

    def get_options_fingerprint(self) -> FingerprintPart:
        return get_value_fingerprint(self.options.render_options.raw_data)


class ColumnMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ColumnMetricResult"
        field_tags = {
            "column_name": {IncludeTags.Parameter},
            "column_type": {IncludeTags.Parameter},
        }

    column_name: str
    # todo: use enum
    column_type: str

    def get_pandas(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict({self.column_name: self.collect_pandas_columns()}, orient="index")
        df.index.name = "column_name"
        return df


ColumnTResult = TypeVar("ColumnTResult", bound=ColumnMetricResult)


class ColumnMetric(Metric[ColumnTResult], Generic[ColumnTResult], abc.ABC):
    column_name: ColumnName

    def __init__(self, column_name: Union[ColumnName, str], options: AnyOptions = None):
        self.column_name = ColumnName.from_any(column_name)
        super().__init__(options)
