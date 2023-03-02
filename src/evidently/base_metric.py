import abc
import logging
from copy import copy
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd

from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.renderers.base_renderer import MetricRenderer
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.visualizations import Distribution

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr
    from pydantic.typing import DictStrAny
    from pydantic.typing import MappingIntStrAny

TResult = TypeVar("TResult")


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
    dataset: DatasetType
    feature_class: Optional[GeneratedFeature]


def additional_feature(feature: GeneratedFeature,
                       feature_name: str) -> ColumnName:
    return ColumnName(
        name=feature.__class__.__name__ + "." + feature_name,
        dataset=DatasetType.ADDITIONAL,
        feature_class=feature,
    )


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    reference_additional_features: Optional[pd.DataFrame]
    current_additional_features: Optional[pd.DataFrame]
    column_mapping: ColumnMapping
    data_definition: DataDefinition

    @staticmethod
    def _get_by_column_name(dataset: pd.DataFrame, additional: pd.DataFrame,
                            column: ColumnName) -> pd.Series:
        if column.dataset == DatasetType.MAIN:
            return dataset[column.name]
        if column.dataset == DatasetType.ADDITIONAL:
            return additional[column.name]
        raise ValueError("unknown column data")

    def get_current_column(self, column: Union[str, ColumnName]) -> pd.Series:
        if isinstance(column, str):
            _column = ColumnName(column, DatasetType.MAIN, None)
        else:
            _column = column
        return self._get_by_column_name(self.current_data,
                                        self.current_additional_features,
                                        _column)

    def get_reference_column(self, column: Union[str, ColumnName]) -> Optional[
        pd.Series]:
        if self.reference_data is None:
            return None
        if isinstance(column, str):
            _column = ColumnName(column, DatasetType.MAIN, None)
        else:
            _column = column
        if self.reference_additional_features is None and _column.dataset == DatasetType.ADDITIONAL:
            return None
        return self._get_by_column_name(self.reference_data,
                                        self.reference_additional_features,
                                        _column)


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
            raise ValueError(
                f"No result found for metric {self} of type {type(self).__name__}")
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
            logging.warning(
                f"unhashable params for {type(self)}. Fallback to unique.")
            return None
        return params

    def required_features(self, data_definition: DataDefinition) -> List[
        GeneratedFeature]:
        required_features = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if issubclass(type(value),
                          ColumnName) and value.feature_class is not None:
                required_features.append(value.feature_class)
        return required_features


from typing import Union

import numpy as np
from pydantic import BaseConfig
from pydantic import BaseModel


class MetricResult(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        dict_include: set = set()
        dict_exclude: set = set()

    if TYPE_CHECKING:
        __config__: ClassVar[Type[Config]] = Config

    def get_dict(self):
        exclude = set(self.__config__.dict_exclude)
        for name, field in self.__fields__.items():
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResultField):
                if not field.type_.__config__.dict_include:
                    exclude.add(name)
        return self.dict(include=self.__config__.dict_include or None, exclude=exclude)


class MetricResultField(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        dict_include: bool = True

    if TYPE_CHECKING:
        __config__: ClassVar[Type[Config]] = Config

    def dict(
        self,
        *,
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        exclude = copy(exclude) or set()

        for name, field in self.__fields__.items():
            if isinstance(field.type_, type) and issubclass(field.type_, MetricResultField):
                if not field.type_.__config__.dict_include:
                    if isinstance(exclude, set):
                        exclude.add(name)
                    elif isinstance(exclude, dict):
                        exclude[name] = True
                    else:
                        raise ValueError("Unknow exclude value type")
        return super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)


class ColumnMetricResult(MetricResult):
    class Config:
        use_enum_values = True

    column_name: str
    column_type: ColumnType


class Distribution2(MetricResultField):
    class Config:
        dict_include = False
    x: Union[np.ndarray, list]
    y: Union[np.ndarray, list]

    @classmethod
    def from_old(cls, d: Distribution):
        if d is None:
            return None
        if isinstance(d, list):
            return cls(x=d[0], y=d[1])
        return cls(x=d.x, y=d.y)  # todo tmp


NewTResult = TypeVar("NewTResult", bound=MetricResult)


class NewMetric(Metric, Generic[NewTResult], abc.ABC):
    pass


ColumnTResult = TypeVar("ColumnTResult", bound=ColumnMetricResult)


class ColumnMetric(NewMetric, Generic[ColumnTResult], abc.ABC):
    column_name: str


class NewMetricRenderer(MetricRenderer, abc.ABC):
    def render_pandas(self, obj: NewMetric) -> pd.DataFrame:
        raise Exception("not implemented")  # not considered abs

    def render_json(self, obj: NewMetric) -> dict:
        return obj.get_result().get_dict()
