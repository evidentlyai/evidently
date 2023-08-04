import abc
from typing import Generic, List, TypeVar

from evidently.base_metric import MetricResult
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently2.core.calculation import Calculation

MR = TypeVar("MR", bound=MetricResult)
class Metric(EvidentlyBaseModel, Generic[MR]):

    # @abc.abstractmethod
    # def get_reference_calculations(self) -> List[Calculation]:
    #     raise NotImplementedError

    @abc.abstractmethod
    def calculate(self, data) -> MR:
        raise NotImplementedError
