from abc import ABC
from typing import ClassVar

from evidently2.core.calculation import CI, CR, Calc, CalculationEngine, CalculationImplementation, InputColumnData
from evidently2.core.spark import is_spark_data


class PandasEngine(CalculationEngine):

    @classmethod
    def can_use_engine(cls, data) -> bool:
        # fixme
        return not is_spark_data(data)


class PandasCalculation(CalculationImplementation, ABC):
    engine :ClassVar = PandasEngine

class PandasInputColumnData(PandasCalculation[InputColumnData]):
    calculation_type :ClassVar = InputColumnData

    @classmethod
    def calculate(cls, self: InputColumnData, data):
        return data[self.column]
