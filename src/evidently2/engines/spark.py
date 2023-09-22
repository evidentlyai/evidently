from abc import ABC
from typing import ClassVar

import numpy as np

from evidently2.calculations.basic import CleanColumn
from evidently2.calculations.basic import DropInf
from evidently2.calculations.basic import Histogram
from evidently2.calculations.basic import IsEmpty
from evidently2.calculations.basic import Mul
from evidently2.calculations.basic import NUnique
from evidently2.calculations.basic import Size
from evidently2.calculations.basic import ValueCounts
from evidently2.core.calculation import CalculationEngine
from evidently2.core.calculation import CalculationImplementation
from evidently2.core.calculation import InputColumnData
from evidently2.core.spark import SparkDataFrame
from evidently2.core.spark import is_spark_data
from evidently2.core.spark import single_column
from evidently.metric_results import Distribution


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


class SparkDropInf(SparkCalculation[DropInf]):
    calculation_type = DropInf

    @classmethod
    def calculate(cls, self: DropInf, data: SparkDataFrame):
        return data.filter(~single_column(data).isin([np.inf, -np.inf]))


class SparkCleanColumn(SparkCalculation[CleanColumn]):
    calculation_type = CleanColumn

    @classmethod
    def calculate(cls, self: CleanColumn, data: SparkDataFrame):
        return data.replace([np.inf, -np.inf], None).dropna()


class SparkSize(SparkCalculation[Size]):
    calculation_type = Size

    @classmethod
    def calculate(cls, self: Size, data: SparkDataFrame):
        return data.count()


class SparkValueCounts(SparkCalculation[ValueCounts]):
    calculation_type = ValueCounts

    @classmethod
    def calculate(cls, self: ValueCounts, data: SparkDataFrame):
        # materialize
        column = single_column(data)
        result = data.groupby(column.alias("_")).count().collect()
        return {r["_"]: r["count"] for r in result}


class SparkMul(SparkCalculation[Mul]):
    calculation_type = Mul

    @classmethod
    def calculate(cls, self: Mul, data: SparkDataFrame):
        return data * self.second.get_result()


class SparkNUnique(SparkCalculation[NUnique]):
    calculation_type = NUnique

    @classmethod
    def calculate(cls, self: NUnique, data: SparkDataFrame):
        from pyspark.sql.functions import count_distinct

        return data.select(count_distinct(single_column(data)).alias("nunique")).first()["nunique"]


class SparkHistogram(SparkCalculation[Histogram]):
    calculation_type = Histogram

    @classmethod
    def calculate(cls, self: Histogram, data: SparkDataFrame):
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
        from pyspark.sql.functions import floor
        from pyspark.sql.functions import max
        from pyspark.sql.functions import min
        from pyspark.sql.functions import when

        column = single_column(data)
        col_range = data.select(min(column).alias("min"), max(column).alias("max")).first()
        min_val, max_val = col_range["min"], col_range["max"]
        step = (max_val - min_val) / self.bins
        hist = (
            data.select(column, floor((column - min_val) / step).alias("bucket"))
            .select(column, when(col("bucket") >= self.bins, self.bins - 1).otherwise(col("bucket")).alias("bucket"))
            .groupby("bucket")
            .count()
        )

        spark = SparkSession.getActiveSession()
        df_buckets = spark.sql(f"select id+1 as bucket from range({self.bins})")
        hist = (
            hist.join(df_buckets, "bucket", "right_outer")
            .selectExpr("bucket", "nvl(count, 0) as count")
            .orderBy("bucket")
        )

        y = [v["count"] for v in hist.select("count").collect()]
        x = [min_val + step * i for i in range(self.bins + 1)]
        return Distribution(x=x, y=y)


class SparkIsEmpty(SparkCalculation[IsEmpty]):
    calculation_type = IsEmpty

    @classmethod
    def calculate(cls, self: IsEmpty, data: SparkDataFrame):
        return data.rdd.isEmpty()
