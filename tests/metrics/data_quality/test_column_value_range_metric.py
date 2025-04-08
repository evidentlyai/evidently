import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.descriptors import TextLength
from evidently.legacy.metric_results import Distribution
from evidently.legacy.metrics import ColumnValueRangeMetric
from evidently.legacy.metrics.data_quality.column_value_range_metric import ColumnValueRangeMetricResult
from evidently.legacy.metrics.data_quality.column_value_range_metric import ValuesInRangeStat
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report
from tests.conftest import smart_assert_equal


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_result",
    (
        (
            pd.DataFrame({"col": []}),
            None,
            ColumnValueRangeMetric(column_name="col", left=0, right=10.3),
            ColumnValueRangeMetricResult(
                column_name="col",
                left=0,
                right=10.3,
                current=ValuesInRangeStat(
                    number_in_range=0,
                    number_not_in_range=0,
                    share_in_range=0,
                    share_not_in_range=0,
                    number_of_values=0,
                    distribution=Distribution(x=np.array([0.0, 1.0]), y=np.array([0])),
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, np.nan, 3, -3.2]}),
            pd.DataFrame({"col": [-1.5, 2, np.nan, 3, 20]}),
            ColumnValueRangeMetric(column_name="col"),
            ColumnValueRangeMetricResult(
                column_name="col",
                left=-1.5,
                right=20,
                current=ValuesInRangeStat(
                    number_in_range=3,
                    number_not_in_range=1,
                    share_in_range=0.75,
                    share_not_in_range=0.25,
                    number_of_values=4,
                    distribution=Distribution(
                        x=np.array(
                            [
                                -3.2,
                                0.11428571428571388,
                                3.428571428571428,
                                6.742857142857143,
                                10.057142857142857,
                                13.37142857142857,
                                16.685714285714287,
                                20.0,
                            ]
                        ),
                        y=np.array([1, 3, 0, 0, 0, 0, 0]),
                    ),
                ),
                reference=ValuesInRangeStat(
                    number_in_range=4,
                    number_not_in_range=0,
                    share_in_range=1,
                    share_not_in_range=0,
                    number_of_values=4,
                    distribution=Distribution(
                        x=np.array(
                            [
                                -3.2,
                                0.11428571428571388,
                                3.428571428571428,
                                6.742857142857143,
                                10.057142857142857,
                                13.37142857142857,
                                16.685714285714287,
                                20.0,
                            ]
                        ),
                        y=np.array([1, 2, 0, 0, 0, 0, 1]),
                    ),
                ),
            ),
        ),
    ),
)
def test_data_quality_values_in_range_metric_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    metric: ColumnValueRangeMetric,
    expected_result: ColumnValueRangeMetricResult,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    result = metric.get_result()

    smart_assert_equal(result, expected_result)


@pytest.mark.parametrize(
    "current_data, reference_data, metric",
    (
        (
            pd.DataFrame({"col": [1, 2, 3, 4, 5, 6]}),
            None,
            ColumnValueRangeMetric(
                column_name="col",
                left=0,
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, 3, 4, 5, 6]}),
            None,
            ColumnValueRangeMetric(
                column_name="col",
                right=0,
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, 3, 4, 5, 6]}),
            None,
            ColumnValueRangeMetric(
                column_name="feature",
                left=0,
            ),
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3, 4, 5, 6]}),
            pd.DataFrame({"col": [1, 2, 3, 4, 5, 6]}),
            ColumnValueRangeMetric(
                column_name="feature",
                right=0,
            ),
        ),
        (
            pd.DataFrame({"feature": ["a", 2, 3, 4, 5, 6]}),
            None,
            ColumnValueRangeMetric(column_name="feature", right=0, left=10),
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3, 4, 5, 6]}),
            pd.DataFrame({"feature": [np.nan, pd.NaT, pd.NA, np.nan, pd.NaT, pd.NA]}),
            ColumnValueRangeMetric(column_name="feature", right=0, left=10),
        ),
    ),
)
def test_data_quality_values_in_range_metric_errors(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnValueRangeMetric
) -> None:
    with pytest.raises(ValueError):
        report = Report(metrics=[metric])
        report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
        metric.get_result()


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValueRangeMetric(
                column_name="col",
                left=0,
                right=10,
            ),
            {
                "column_name": "col",
                "current": {
                    "number_in_range": 3,
                    "number_not_in_range": 0,
                    "number_of_values": 3,
                    "share_in_range": 1.0,
                    "share_not_in_range": 0.0,
                },
                "left": 0,
                "right": 10,
                "reference": None,
            },
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            pd.DataFrame({"col": [10, 20, 3.5]}),
            ColumnValueRangeMetric(
                column_name="col",
            ),
            {
                "column_name": "col",
                "current": {
                    "number_in_range": 0,
                    "number_not_in_range": 3,
                    "number_of_values": 3,
                    "share_in_range": 0.0,
                    "share_not_in_range": 1.0,
                },
                "left": 3.5,
                "reference": {
                    "number_in_range": 3,
                    "number_not_in_range": 0,
                    "number_of_values": 3,
                    "share_in_range": 1.0,
                    "share_not_in_range": 0.0,
                },
                "right": 20.0,
            },
        ),
        (
            pd.DataFrame({"col2": ["a", "aa", "aaa"]}),
            pd.DataFrame({"col2": ["a", "aa", "aaa"]}),
            ColumnValueRangeMetric(
                column_name=TextLength().for_column("col2"),
            ),
            {
                "column_name": "Text Length for col2",
                "current": {
                    "number_in_range": 3,
                    "number_not_in_range": 0,
                    "number_of_values": 3,
                    "share_in_range": 1.0,
                    "share_not_in_range": 0.0,
                },
                "left": 1.0,
                "reference": {
                    "number_in_range": 3,
                    "number_not_in_range": 0,
                    "number_of_values": 3,
                    "share_in_range": 1.0,
                    "share_not_in_range": 0.0,
                },
                "right": 3.0,
            },
        ),
    ),
)
def test_data_quality_values_in_range_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnValueRangeMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(
        current_data=current_data,
        reference_data=reference_data,
        column_mapping=ColumnMapping(numerical_features=["col"]),
    )
    assert report.show()
    result_json = report.json()
    assert len(result_json) > 0
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "ColumnValueRangeMetric"
    assert result["metrics"][0]["result"] == expected_json
