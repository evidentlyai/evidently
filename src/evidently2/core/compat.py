import abc
from typing import ClassVar
from typing import TypeVar

import pandas as pd

from evidently2.core.calculation import Calculation
from evidently2.core.calculation import Constant
from evidently2.core.calculation import DataType
from evidently2.core.calculation import InputData
from evidently2.core.calculation import create_calculation_from_callable
from evidently2.core.metric import MR
from evidently2.core.metric import Metric
from evidently2.core.metric import MetricResultCalculation
from evidently.base_metric import ColumnName
from evidently.base_metric import MetricResult


class InputData2:
    def __init__(self, input_data: InputData):
        self.input_data = input_data

    @property
    def reference_data(self) -> DataType:
        return self.input_data.reference_data.get_result()

    @property
    def current_data(self) -> DataType:
        return self.input_data.current_data.get_result()

    def get_current_column(self, column_name: ColumnName) -> pd.Series:
        return self.input_data.get_current_column(column_name).get_result()

    def get_reference_column(self, column_name: ColumnName) -> pd.Series:
        return self.input_data.get_reference_column(column_name).get_result()


MR2 = TypeVar("MR2", bound=MetricResult)


class Metric2(Metric[MR2]):
    _calculation: ClassVar[Calculation]

    def __init_subclass__(cls):
        cls._calculation = create_calculation_from_callable(cls.calculate2)
        super().__init_subclass__()

    @abc.abstractmethod
    def calculate2(self, data: InputData2) -> MR2:
        raise NotImplementedError

    def calculate(self, data) -> MetricResultCalculation[MR]:
        return self._calculation(instance=self, input_data=Constant(value=InputData2(input_data=data)))
