import abc
from typing import Any, Generic, Optional, TypeVar

import pandas as pd

from evidently.base_metric import ColumnName
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition


class CalculationResult(EvidentlyBaseModel):
    pass

CI = TypeVar("CI")
CR = TypeVar("CR")

DataType = pd.DataFrame

class _CalculationBase(EvidentlyBaseModel):
    @abc.abstractmethod
    def get_result(self):
        raise NotImplementedError

class Calculation(_CalculationBase, Generic[CI, CR]):
    input_data: "_CalculationBase"

    # def __init__(self, input_data: _CalculationBase, **data):
    #     super().__init__(input_data=input_data, **data)

    @abc.abstractmethod
    def calculate(self, data: CI) -> CR:
        raise NotImplementedError

    def get_result(self):
        return self.calculate(self.input_data.get_result())


class InputValue(_CalculationBase):
    data: Any

    def get_result(self):
        return self.data

class InputData:
    def __init__(self, current_data, reference_data, data_definition: DataDefinition):
        self._current_data = current_data
        self._reference_data = reference_data
        self.data_definition = data_definition

    @property
    def reference_data(self) -> Optional[_CalculationBase]:
        return None if self._reference_data is None else InputValue(data=self._reference_data)

    @property
    def current_data(self) -> _CalculationBase:
        return InputValue(data=self._current_data)

    def get_current_column(self, column_name: ColumnName) -> "InputColumnData":
        return InputColumnData(input_data=self.current_data, column=column_name.name)

    def get_reference_column(self, column_name: ColumnName) -> "InputColumnData":
        return InputColumnData(input_data=self.reference_data, column=column_name.name)


class InputColumnData(Calculation):
    input_data: InputValue
    column: str

    def calculate(self, data: CI) -> CR:
        return data[self.column]