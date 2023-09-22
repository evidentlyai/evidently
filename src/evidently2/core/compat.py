import abc
from typing import ClassVar
from typing import Optional
from typing import TypeVar

import pandas as pd

from evidently2.core.calculation import Calculation
from evidently2.core.calculation import Constant
from evidently2.core.calculation import DataType
from evidently2.core.calculation import InputData as NewInputData
from evidently2.core.calculation import NoInputError
from evidently2.core.calculation import create_calculation_from_callable
from evidently2.core.metric import MR
from evidently2.core.metric import BaseMetric
from evidently2.core.metric import MetricResultCalculation
from evidently.base_metric import ColumnName
from evidently.base_metric import InputData
from evidently.base_metric import MetricResult


class CompatInputData:
    def __init__(self, input_data: NewInputData):
        self.input_data = input_data

    @property
    def reference_data(self) -> Optional[DataType]:
        try:
            return self.input_data.reference_data.get_result()
        except NoInputError:
            return None

    @property
    def current_data(self) -> DataType:
        return self.input_data.current_data.get_result()

    def get_current_column(self, column_name: ColumnName) -> pd.Series:
        return self.input_data.get_current_column(column_name).get_result()

    def get_reference_column(self, column_name: ColumnName) -> pd.Series:
        return self.input_data.get_reference_column(column_name).get_result()


MR2 = TypeVar("MR2", bound=MetricResult)


class Metric(BaseMetric[MR2]):
    _calculation: ClassVar[Calculation]

    def __init_subclass__(cls):
        cls._calculation = create_calculation_from_callable(cls.calculate)
        super().__init_subclass__()

    @abc.abstractmethod
    def calculate(self, data: InputData) -> MR2:
        raise NotImplementedError

    def get_calculation(self, data) -> MetricResultCalculation[MR]:
        return self._calculation(instance=self, input_data=Constant(value=CompatInputData(input_data=data)))
