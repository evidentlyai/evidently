import numpy as np
import pandas as pd

from evidently.metric_results import Distribution
from evidently2.core.calculation import CI, CR, Calculation, NoInputError, _CalculationBase
from evidently2.core.spark import SparkDataFrame, is_spark_data, single_column


class DropInf(Calculation):
    def calculate(self, data: CI) -> CR:
        return data[np.isfinite(data)]

    def calculate_spark(self, data: SparkDataFrame):
        return data.filter(~single_column(data).isin([np.inf, -np.inf]))


class CleanColumn(Calculation[pd.Series, pd.Series]):
    def calculate(self, data: pd.Series) -> pd.Series:
        return data.replace([-np.inf, np.inf], np.nan).dropna()

    # def calculate_spark(self, data):
    def calculate_spark(self, data: SparkDataFrame):
        return data.replace([np.inf, -np.inf], None).dropna()

    @property
    def empty(self):
        # todo: can we do this lazy?
        try:
            result = self.get_result()
            if is_spark_data(result):
                return result.rdd.isEmpty()
            return result.empty
        except NoInputError:
            return False


class DropNA(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.dropna()


class Unique(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.unique()


class CreateSet(Calculation):
    def calculate(self, data: CI) -> CR:
        return set(data)


class UnionList(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return list(data | self.second.get_result())


class Size(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.shape[0]

    def calculate_spark(self, data: SparkDataFrame):
        return data.count()


class Div(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return data / self.second.get_result()

    # def calculate_spark(self, data: SparkDataFrame):
    #     return data / self.second.get_result()


class ValueCounts(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.value_counts()

    def calculate_spark(self, data: SparkDataFrame):
        # materialize
        column = single_column(data)
        result = data.groupby(column.alias("_")).count().collect()
        return {r["_"]: r["count"] for r in result}


class Mul(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return data * self.second.get_result()

    def calculate_spark(self, data: SparkDataFrame):
        return data * self.second.get_result()


class MultDict(Calculation):
    mul: Calculation

    def calculate(self, data: CI) -> CR:
        m = self.mul.get_result()
        return {k: v * m for k, v in data.items()}

    # def calculate_spark(self, data: SparkDataFrame):
    #     m = self.mul.get_result()
    #     return {k: v * m for k, v in data.items()}


class LessThen(Calculation):
    second: _CalculationBase

    def calculate(self, data: CI) -> CR:
        return data < self.second.get_result()


class NUnique(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.nunique()

    def calculate_spark(self, data: SparkDataFrame):
        from pyspark.sql.functions import count_distinct

        return data.select(count_distinct(single_column(data)).alias("nunique")).first()["nunique"]


class Histogram(Calculation[pd.Series, Distribution]):
    bins: int
    density: bool

    def __init__(self, input_data: _CalculationBase, bins: int, density: bool):
        super().__init__(input_data=input_data, bins=bins, density=density)

    def calculate(self, data: pd.Series) -> Distribution:
        y, x = [
            t.tolist()
            for t in np.histogram(
                data,
                bins=self.bins,
                density=self.density,
            )
        ]
        return Distribution(x=x, y=y)

    def calculate_spark(self, data: SparkDataFrame):
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


class Mask(Calculation[pd.Series, pd.Series]):
    mask: Calculation

    def __init__(self, input_data: _CalculationBase, mask: Calculation):
        super().__init__(input_data=input_data, mask=mask)

    def calculate(self, data: CI) -> CR:
        return data[self.mask.get_result()]


class IsFinite(Calculation[pd.Series, pd.Series]):
    def __init__(self, input_data: _CalculationBase):
        super().__init__(input_data=input_data)

    def calculate(self, data: CI) -> CR:
        return np.isfinite(data)
