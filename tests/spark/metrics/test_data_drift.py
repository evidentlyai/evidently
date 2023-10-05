import pandas as pd
import pytest
from pyspark.sql import SparkSession

from evidently import ColumnMapping
from evidently.base_metric import ColumnName
from evidently.metrics import ColumnDriftMetric
from evidently.report import Report
from evidently.spark.engine import SparkEngine
from tests.conftest import smart_assert_equal


@pytest.mark.parametrize("metric", [
    ColumnDriftMetric(column_name=ColumnName.from_any("a")),
    ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="wasserstein"),
    ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="psi"),
    ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="jensenshannon")
])
def test_column_data_drift(metric):
    from evidently.options.data_drift import DataDriftOptions
    DataDriftOptions.__fields__["nbinsx"].default = 2

    ref_pd = pd.DataFrame([{"a": 0}, {"a": 1}, {"a": 2}])
    cur_pd = pd.DataFrame([{"a": 0}, {"a": 0}, {"a": 0}])

    session = SparkSession.builder.getOrCreate()
    ref = session.createDataFrame(ref_pd)
    cur = session.createDataFrame(cur_pd)

    column_mapping = ColumnMapping(numerical_features=["a"])

    report = Report(metrics=[metric])
    report.run(reference_data=ref_pd, current_data=cur_pd, column_mapping=column_mapping)
    report._inner_suite.raise_for_error()

    res1 = report.as_dict(include_render=True)["metrics"][0]["result"]

    spark_report = Report(metrics=[metric.copy(deep=True)])
    spark_report.run(reference_data=ref, current_data=cur, column_mapping=column_mapping, engine=SparkEngine)
    spark_report._inner_suite.raise_for_error()

    res2 = spark_report.as_dict(include_render=True)["metrics"][0]["result"]
    smart_assert_equal(res2, res1)
