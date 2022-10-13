from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DataQualityValueListMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_quality.data_quality_value_list_metric import DataQualityValueListMetricsResult
from evidently.metrics.data_quality.data_quality_value_list_metric import ValueListStat


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, expected_result",
    (
        (
            pd.DataFrame({"category_feature": []}),
            None,
            DataQualityValueListMetric(column_name="category_feature", values=["test"]),
            DataQualityValueListMetricsResult(
                column_name="category_feature",
                values=["test"],
                current=ValueListStat(
                    number_in_list=0,
                    number_not_in_list=0,
                    share_in_list=0,
                    share_not_in_list=0,
                    values_count={},
                    rows_count=0,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [np.NaN, np.NaN, np.NaN]}),
            None,
            DataQualityValueListMetric(column_name="category_feature", values=["test"]),
            DataQualityValueListMetricsResult(
                column_name="category_feature",
                values=["test"],
                current=ValueListStat(
                    number_in_list=0,
                    number_not_in_list=3,
                    share_in_list=0,
                    share_not_in_list=1,
                    values_count={},
                    rows_count=3,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [1, np.NaN, 1, 2]}),
            None,
            DataQualityValueListMetric(column_name="category_feature", values=[1, 2, 3]),
            DataQualityValueListMetricsResult(
                column_name="category_feature",
                values=[1, 2, 3],
                current=ValueListStat(
                    number_in_list=3,
                    number_not_in_list=1,
                    share_in_list=0.75,
                    share_not_in_list=0.25,
                    values_count={1: 2, 2: 1},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            DataQualityValueListMetric(column_name="category_feature", values=["d"]),
            DataQualityValueListMetricsResult(
                column_name="category_feature",
                values=["d"],
                current=ValueListStat(
                    number_in_list=1,
                    number_not_in_list=3,
                    share_in_list=0.25,
                    share_not_in_list=0.75,
                    values_count={"n": 2, "p": 1, "d": 1},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            DataQualityValueListMetric(column_name="numerical_feature", values=[2]),
            DataQualityValueListMetricsResult(
                column_name="numerical_feature",
                values=[2],
                current=ValueListStat(
                    number_in_list=2,
                    number_not_in_list=2,
                    share_in_list=0.5,
                    share_not_in_list=0.5,
                    values_count={2: 2, 432: 1, 0: 1},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            DataQualityValueListMetric(column_name="category_feature"),
            DataQualityValueListMetricsResult(
                column_name="category_feature",
                values=["n", "d", "p"],
                current=ValueListStat(
                    number_in_list=4,
                    number_not_in_list=0,
                    share_in_list=1.0,
                    share_not_in_list=0.0,
                    values_count={"n": 2, "d": 1, "p": 1},
                    rows_count=4,
                ),
                reference=ValueListStat(
                    number_in_list=4,
                    number_not_in_list=0,
                    share_in_list=1.0,
                    share_not_in_list=0.0,
                    values_count={"n": 2, "d": 1, "p": 1},
                    rows_count=4,
                ),
            ),
        ),
    ),
)
def test_data_quality_value_list_metric_success(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: DataQualityValueListMetric,
    expected_result: DataQualityValueListMetricsResult,
) -> None:
    data_mapping = ColumnMapping()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result == expected_result
