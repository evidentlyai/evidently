from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.utils.spark import fixup_pandas_df_for_big_data
from tests.utils.spark import convert_pandas_to_spark_df_if_necessary


@pytest.mark.parametrize(
    "pandas_df",
    [
        pytest.param(pd.DataFrame({"feature": [1, 2, 3]}), id="all int"),
        pytest.param(pd.DataFrame({"feature": ["a", 1, 2]}), id="str then int"),
        pytest.param(pd.DataFrame({"feature": [1, 2, "a"]}), id="int then str"),
        pytest.param(pd.DataFrame({"feature": ["a", "b", "c"]}), id="all str"),
    ],
)
def test_spark_dataset_conversion_raise_no_error(pandas_df: pd.DataFrame, spark_session):
    # TODO(aadral): consider global configuration for optimization
    # spark_session.conf.set("spark.sql.execution.arrow.enabled", True)

    # TODO(aadral): consider usage of pandas schema directly, otherwise Spark will iterate
    # over each Row of RDD to infer schema
    # https://spark.apache.org/docs/latest/api/python/user_guide/pandas_on_spark/types.html
    # see: #type-casting-between-pandas-and-pandas-api-on-spark

    fixup_pandas_df_for_big_data(pandas_df)
    spark_df = spark_session.createDataFrame(pandas_df, samplingRatio=1.0)
    assert spark_df is not None


def test_spark_quantile(spark_session):
    # pandas uses linear approx: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.quantile.html
    # spark uses approx (sample), but when accuracy is high it is comparable to pandas "highest"
    # https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/api/pyspark.pandas.DataFrame.quantile.html
    pandas_df = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    quantile = 0.5

    fixup_pandas_df_for_big_data(pandas_df)
    spark_df = spark_session.createDataFrame(pandas_df)
    spark_pandas_df = spark_df.pandas_api()

    spark_column = spark_pandas_df["numerical_feature"]
    spark_quantile = spark_column.quantile(quantile)

    pandas_highest_quantile = spark_column.to_pandas().quantile(quantile, interpolation="higher")
    assert 2.0 == pytest.approx(pandas_highest_quantile)
    assert 2.0 == pytest.approx(spark_quantile)

    # this one will fail
    assert 1.5 == pytest.approx(spark_quantile)


def test_quantile(pandas_or_spark_session):
    df = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    df = convert_pandas_to_spark_df_if_necessary(df, pandas_or_spark_session)

    column = df["numerical_feature"]
    quantile = 0.5

    calculated_quantile = column.quantile(quantile)
    assert 1.5 == pytest.approx(calculated_quantile)


@pytest.mark.parametrize(
    "current",
    (
        pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]}),
    )
)
def test_quantile_with_parametrize(current: pd.DataFrame, pandas_or_spark_session):
    current = convert_pandas_to_spark_df_if_necessary(current, pandas_or_spark_session)
    quantile = 0.5

    column = current["numerical_feature"]
    calculated_quantile = column.quantile(quantile)
    assert 1.5 == pytest.approx(calculated_quantile)


def test_spark_quantile_with_input_data(pandas_or_spark_session):
    from evidently import ColumnMapping
    from evidently.base_metric import InputData
    from evidently.utils.data_preprocessing import create_data_definition

    current = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    reference = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    quantile = 0.5

    current = convert_pandas_to_spark_df_if_necessary(current, pandas_or_spark_session)
    reference = convert_pandas_to_spark_df_if_necessary(reference, pandas_or_spark_session)

    column_mapping = ColumnMapping()
    data_definition = create_data_definition(reference, current, column_mapping)
    data = InputData(reference, current, None, None, column_mapping, data_definition)

    column_type, current_column, reference_column = data.get_data("numerical_feature")
    current_quantile = current_column.quantile(quantile)
    assert 1.5 == pytest.approx(current_quantile)


def test_spark_quantile_with_report_breakdown(pandas_or_spark_session):
    from evidently import ColumnMapping
    from evidently.base_metric import InputData
    from evidently.metrics import ColumnQuantileMetric
    from evidently.report import Report
    from evidently.utils.data_preprocessing import create_data_definition

    current = pd.DataFrame({"numerical_feature": [0, 4, 1, 2, np.NaN]})
    reference = pd.DataFrame({"numerical_feature": [0, 2, 2, 2, 0]})
    column_mapping = ColumnMapping()

    current = convert_pandas_to_spark_df_if_necessary(current, pandas_or_spark_session)
    reference = convert_pandas_to_spark_df_if_necessary(reference, pandas_or_spark_session)

    metric = ColumnQuantileMetric(column_name="numerical_feature", quantile=0.5)

    # report = Report(metrics=[metric])

    data_definition = create_data_definition(reference, current, column_mapping)
    data = InputData(reference, current, None, None, column_mapping, data_definition)

    # first level deep
    # report._first_level_metrics.append(metric)
    # report._inner_suite.add_metric(metric)
    # report._inner_suite.run_calculate(data)

    # second level deep
    # from evidently.suite.base_suite import Suite
    # _inner_suite = Suite(None)
    # _inner_suite.add_metric(metric)
    # _inner_suite.run_calculate(data)

    # third level deep
    # metric_result = metric.calculate(data)
    # assert 1.5 == pytest.approx(metric_result.current.value)

    column_type, current_column, reference_column = data.get_data(metric.column)
    current_quantile = current_column.quantile(metric.quantile)
    assert 1.5 == pytest.approx(current_quantile)
