from abc import ABC
from typing import ClassVar

import numpy as np

from evidently.metric_results import Distribution
from evidently2.calculations.basic import CleanColumn, DropInf, Histogram, Mul, NUnique, Size, ValueCounts
from evidently2.core.calculation import CalculationEngine, CalculationImplementation, InputColumnData
from evidently2.core.spark import SparkDataFrame, is_spark_data, single_column


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
    @classmethod
    def calculate(cls, self: DropInf, data: SparkDataFrame):
        return data.filter(~single_column(data).isin([np.inf, -np.inf]))


class SparkCleanColumn(SparkCalculation[CleanColumn]):
    @classmethod
    def calculate(cls, self: CleanColumn, data: SparkDataFrame):
        return data.replace([np.inf, -np.inf], None).dropna()

    # @property
    # def empty(self):
    #     # todo: can we do this lazy?
    #     try:
    #         result = self.get_result()
    #         if is_spark_data(result):
    #             return result.rdd.isEmpty()
    #         return result.empty
    #     except NoInputError:
    #         return False


class SparkSize(SparkCalculation[Size]):
    @classmethod
    def calculate(cls, self: Size, data: SparkDataFrame):
        return data.count()


class SparkValueCounts(SparkCalculation[ValueCounts]):
    @classmethod
    def calculate(cls, self: ValueCounts, data: SparkDataFrame):
        # materialize
        column = single_column(data)
        result = data.groupby(column.alias("_")).count().collect()
        return {r["_"]: r["count"] for r in result}


class SparkMul(SparkCalculation[Mul]):
    @classmethod
    def calculate(cls, self: Mul, data: SparkDataFrame):
        return data * self.second.get_result()


class SparkNUnique(SparkCalculation[NUnique]):
    @classmethod
    def calculate(cls, self: NUnique, data: SparkDataFrame):
        from pyspark.sql.functions import count_distinct

        return data.select(count_distinct(single_column(data)).alias("nunique")).first()["nunique"]


class SparkHistogram(SparkCalculation[Histogram]):
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
