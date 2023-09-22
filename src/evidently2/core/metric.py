import abc
from typing import Generic
from typing import Type
from typing import TypeVar

from evidently2.core.calculation import Calculation
from evidently.base_metric import MetricResult
from evidently.pydantic_utils import EvidentlyBaseModel

MR = TypeVar("MR", bound=MetricResult)


class MetricResultCalculation(EvidentlyBaseModel, Generic[MR]):
    @classmethod
    def result_type(cls) -> Type[MetricResult]:
        return cls.__orig_bases__[0].__args__[0]  # type: ignore[attr-defined]

    def get_result(self) -> MR:
        cls = self.result_type()
        kwargs = {k: v if not isinstance(v, Calculation) else v.get_result() for k, v in self.__dict__.items()}
        return cls(**kwargs)


class ColumnMetricResultCalculation(MetricResultCalculation, Generic[MR]):
    column_name: str
    # todo: use enum
    column_type: str


class BaseMetric(EvidentlyBaseModel, Generic[MR]):
    @abc.abstractmethod
    def get_calculation(self, data) -> MetricResultCalculation[MR]:
        raise NotImplementedError
