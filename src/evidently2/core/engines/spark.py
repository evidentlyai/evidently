from abc import ABC
from typing import ClassVar

from evidently2.core.calculation import CalculationEngine, CalculationImplementation, InputColumnData
from evidently2.core.spark import is_spark_data


class SparkEngine(CalculationEngine):
    @classmethod
    def can_use_engine(cls, data) -> bool:
        return is_spark_data(data)


class SparkCalculation(CalculationImplementation, ABC):
    engine: ClassVar = SparkEngine


class SparkInputColumnData(SparkCalculation[InputColumnData]):
    calculation_type = InputColumnData

    @classmethod
    def calculate(cls, self: InputColumnData, data):
        from pyspark.sql.functions import col

        return data.select(col(self.column).alias("column"))