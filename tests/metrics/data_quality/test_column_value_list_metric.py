import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ColumnValueListMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_quality.column_value_list_metric import ColumnValueListMetricResult
from evidently.metrics.data_quality.column_value_list_metric import ValueListStat
from evidently.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, expected_result",
    (
        (
            pd.DataFrame({"category_feature": []}),
            None,
            ColumnValueListMetric(column_name="category_feature", values=["test"]),
            ColumnValueListMetricResult(
                column_name="category_feature",
                values=["test"],
                current=ValueListStat(
                    number_in_list=0,
                    number_not_in_list=0,
                    share_in_list=0,
                    share_not_in_list=0,
                    values_in_list={},
                    values_not_in_list={},
                    rows_count=0,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [np.NaN, np.NaN, np.NaN]}),
            None,
            ColumnValueListMetric(column_name="category_feature", values=["test"]),
            ColumnValueListMetricResult(
                column_name="category_feature",
                values=["test"],
                current=ValueListStat(
                    number_in_list=0,
                    number_not_in_list=3,
                    share_in_list=0,
                    share_not_in_list=1,
                    values_in_list={"test": 0},
                    values_not_in_list={},
                    rows_count=3,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [1, np.NaN, 1, 2]}),
            None,
            ColumnValueListMetric(column_name="category_feature", values=[1, 2, 3]),
            ColumnValueListMetricResult(
                column_name="category_feature",
                values=[1, 2, 3],
                current=ValueListStat(
                    number_in_list=3,
                    number_not_in_list=1,
                    share_in_list=0.75,
                    share_not_in_list=0.25,
                    values_in_list={2: 1, 1: 2, 3: 0},
                    values_not_in_list={},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            ColumnValueListMetric(column_name="category_feature", values=["d"]),
            ColumnValueListMetricResult(
                column_name="category_feature",
                values=["d"],
                current=ValueListStat(
                    number_in_list=1,
                    number_not_in_list=3,
                    share_in_list=0.25,
                    share_not_in_list=0.75,
                    values_in_list={"d": 1},
                    values_not_in_list={"n": 2, "p": 1},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            ColumnValueListMetric(column_name="numerical_feature", values=[2]),
            ColumnValueListMetricResult(
                column_name="numerical_feature",
                values=[2],
                current=ValueListStat(
                    number_in_list=2,
                    number_not_in_list=2,
                    share_in_list=0.5,
                    share_not_in_list=0.5,
                    values_in_list={2: 2},
                    values_not_in_list={432: 1, 0: 1},
                    rows_count=4,
                ),
                reference=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            ColumnValueListMetric(column_name="category_feature"),
            ColumnValueListMetricResult(
                column_name="category_feature",
                values=["n", "d", "p"],
                current=ValueListStat(
                    number_in_list=4,
                    number_not_in_list=0,
                    share_in_list=1.0,
                    share_not_in_list=0.0,
                    values_in_list={"n": 2, "p": 1, "d": 1},
                    values_not_in_list={},
                    rows_count=4,
                ),
                reference=ValueListStat(
                    number_in_list=4,
                    number_not_in_list=0,
                    share_in_list=1.0,
                    share_not_in_list=0.0,
                    values_in_list={"n": 2, "p": 1, "d": 1},
                    values_not_in_list={},
                    rows_count=4,
                ),
            ),
        ),
    ),
)
def test_data_quality_value_list_metric_success(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnValueListMetric,
    expected_result: ColumnValueListMetricResult,
) -> None:
    data_mapping = ColumnMapping()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, error_message",
    (
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            ColumnValueListMetric(column_name="test", values=[1]),
            "Column 'test' is not in current data.",
        ),
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, 3]}),
            ColumnValueListMetric(column_name="test"),
            "Column 'test' is not in reference data.",
        ),
        (
            pd.DataFrame({"test": ["a", "b", "c"]}),
            None,
            ColumnValueListMetric(column_name="test"),
            "Reference or values list should be present.",
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"feature": [1, 2, "a"]}),
            ColumnValueListMetric(column_name="feature", values=[]),
            "Values list should not be empty.",
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"feature": [np.NaN]}),
            ColumnValueListMetric(column_name="feature", values=[]),
            "Values list should not be empty.",
        ),
    ),
)
def test_data_quality_value_list_metric_value_errors(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnValueListMetric,
    error_message: str,
) -> None:
    data_mapping = ColumnMapping()

    with pytest.raises(ValueError) as error:
        metric.calculate(
            data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
        )

    assert error.value.args[0] == error_message


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnValueListMetric(column_name="col", values=[1]),
            {
                "column_name": "col",
                "current": {
                    "number_in_list": 1,
                    "number_not_in_list": 2,
                    "rows_count": 3,
                    "share_in_list": 0.3333333333333333,
                    "share_not_in_list": 0.6666666666666666,
                    "values_in_list": {"1": 1},
                    "values_not_in_list": {"2": 1, "3": 1},
                },
                "reference": None,
                "values": [1],
            },
        ),
        (
            pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, 3.5]}),
            pd.DataFrame(
                {
                    "col1": [10, 20, 3.5],
                    "col2": [1, 2, 3],
                }
            ),
            ColumnValueListMetric(column_name="col1"),
            {
                "column_name": "col1",
                "current": {
                    "number_in_list": 0,
                    "number_not_in_list": 3,
                    "rows_count": 3,
                    "share_in_list": 0.0,
                    "share_not_in_list": 1.0,
                    "values_in_list": {"10.0": 0, "20.0": 0, "3.5": 0},
                    "values_not_in_list": {"1": 1, "2": 1, "3": 1},
                },
                "reference": {
                    "number_in_list": 3,
                    "number_not_in_list": 0,
                    "rows_count": 3,
                    "share_in_list": 1.0,
                    "share_not_in_list": 0.0,
                    "values_in_list": {"10.0": 1, "20.0": 1, "3.5": 1},
                    "values_not_in_list": {},
                },
                "values": [10.0, 20.0, 3.5],
            },
        ),
    ),
)
def test_data_quality_value_list_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnValueListMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnValueListMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnValueListMetric"] == expected_json
