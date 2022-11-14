import json

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics.data_quality.column_value_range_metric import ColumnValueRangeMetricResult
from evidently.metrics.data_quality.column_value_range_metric import ValuesInRangeStat
from evidently.report import Report
from evidently.utils.visualizations import Distribution


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
                ),
                reference=None,
                current_distribution=Distribution(x=[], y=[]),
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, np.NAN, 3, -3.2]}),
            pd.DataFrame({"col": [-1.5, 2, np.NAN, 3, 20]}),
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
                ),
                reference=ValuesInRangeStat(
                    number_in_range=4,
                    number_not_in_range=0,
                    share_in_range=1,
                    share_not_in_range=0,
                    number_of_values=4,
                ),
                current_distribution=Distribution(x=[], y=[]),
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
    assert result == expected_result


@pytest.mark.parametrize(
    "current_data, reference_data, metric",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValueRangeMetric(
                column_name="col",
                left=0,
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValueRangeMetric(
                column_name="col",
                right=0,
            ),
        ),
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValueRangeMetric(
                column_name="feature",
                left=0,
            ),
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"col": [1, 2, 3]}),
            ColumnValueRangeMetric(
                column_name="feature",
                right=0,
            ),
        ),
        (
            pd.DataFrame({"feature": ["a", 2, 3]}),
            None,
            ColumnValueRangeMetric(column_name="feature", right=0, left=10),
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"feature": [np.NAN, pd.NaT, pd.NA]}),
            ColumnValueRangeMetric(column_name="feature", right=0, left=10),
        ),
    ),
)
def test_data_quality_values_in_range_metric_errors(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    metric: ColumnValueRangeMetric,
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
    ),
)
def test_data_quality_values_in_range_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnValueRangeMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnValueRangeMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnValueRangeMetric"] == expected_json
