import sys
from typing import Callable
from typing import List

import numpy as np
import pandas as pd
import pytest
from pyspark.sql import SparkSession

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.metric_results import DatasetColumns
from evidently.legacy.metric_results import DatasetUtilityColumns
from evidently.legacy.metrics import ColumnDriftMetric
from evidently.legacy.metrics import DataDriftTable
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report
from evidently.legacy.spark.engine import SparkEngine
from evidently.legacy.tests.utils import approx
from tests.conftest import slow
from tests.conftest import smart_assert_equal


@slow
@pytest.mark.skipif(
    sys.platform.startswith("win") or sys.platform == "darwin",
    reason="skip spark on Windows and MacOS",
)
@pytest.mark.parametrize(
    "metric,column_mapping,result_adjust",
    [
        (ColumnDriftMetric(column_name=ColumnName.from_any("a")), ColumnMapping(numerical_features=["a", "b"]), {}),
        (
            ColumnDriftMetric(column_name=ColumnName.from_any("a")),
            ColumnMapping(categorical_features=["a", "b"], target_names=[0, 1, 2], target="a"),
            {},
        ),
        (
            ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="wasserstein"),
            ColumnMapping(numerical_features=["a", "b"]),
            {"drift_score": lambda x: approx(x, absolute=0.05)},
        ),
        (
            ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="psi"),
            ColumnMapping(numerical_features=["a", "b"]),
            {},
        ),
        (
            ColumnDriftMetric(column_name=ColumnName.from_any("a"), stattest="jensenshannon"),
            ColumnMapping(numerical_features=["a", "b"]),
            {},
        ),
        (
            DataDriftTable(num_stattest="jensenshannon"),
            ColumnMapping(numerical_features=["a", "b"]),
            {
                "drift_by_columns.a.current.correlations": lambda x: None,
                "drift_by_columns.a.reference.correlations": lambda x: None,
                "drift_by_columns.b.current.correlations": lambda x: None,
                "drift_by_columns.b.reference.correlations": lambda x: None,
                # todo
                "dataset_columns": lambda x: DatasetColumns(
                    utility_columns=DatasetUtilityColumns(),
                    target_type=None,
                    num_feature_names=[],
                    cat_feature_names=[],
                    text_feature_names=[],
                    datetime_feature_names=[],
                    target_names=[],
                    task=None,
                ),
            },
        ),
        (
            DataDriftTable(num_stattest="jensenshannon", cat_stattest="chisquare"),
            ColumnMapping(numerical_features=["a"], categorical_features=["b"]),
            {
                "drift_by_columns.b.current.distribution.x": lambda x: np.array(list(reversed(x))),
                "drift_by_columns.b.current.distribution.y": lambda x: np.array(list(reversed(x))),
                "drift_by_columns.a.current.correlations": lambda x: None,
                "drift_by_columns.a.reference.correlations": lambda x: None,
                "drift_by_columns.b.current.correlations": lambda x: None,
                "drift_by_columns.b.reference.correlations": lambda x: None,
                # todo
                "dataset_columns": lambda x: DatasetColumns(
                    utility_columns=DatasetUtilityColumns(),
                    target_type=None,
                    num_feature_names=[],
                    cat_feature_names=[],
                    text_feature_names=[],
                    datetime_feature_names=[],
                    target_names=[],
                    task=None,
                ),
            },
        ),
    ],
)
def test_column_data_drift(metric, column_mapping, result_adjust):
    from evidently.legacy.options.data_drift import DataDriftOptions

    DataDriftOptions.__fields__["nbinsx"].default = 2

    ref_pd = pd.DataFrame({"a": [0, 1, 2], "b": [1, 1, 1]})
    cur_pd = pd.DataFrame({"a": [0, 0, 0], "b": [0, 1, 1]})

    session = SparkSession.builder.getOrCreate()
    ref = session.createDataFrame(ref_pd)
    cur = session.createDataFrame(cur_pd)

    report = Report(metrics=[metric])
    report.run(reference_data=ref_pd, current_data=cur_pd, column_mapping=column_mapping)
    report._inner_suite.raise_for_error()

    res1 = report._first_level_metrics[0].get_result().dict()

    spark_report = Report(metrics=[metric.copy(deep=True)])
    spark_report.run(reference_data=ref, current_data=cur, column_mapping=column_mapping, engine=SparkEngine)
    spark_report._inner_suite.raise_for_error()

    res2 = spark_report._first_level_metrics[0].get_result().dict()

    for path, adj in result_adjust.items():
        recursive_adjust(res1, path.split("."), adj)
    smart_assert_equal(res2, res1)

    spark_report.show()


def recursive_adjust(obj, path: List[str], adj: Callable):
    p, *path = path
    if len(path) == 0:
        obj[p] = adj(obj[p])
        return
    recursive_adjust(obj[p], path, adj)
