import json
from typing import Optional

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_quality.column_distribution_metric import ColumnDistributionMetric
from evidently.metrics.data_quality.column_distribution_metric import ColumnDistributionMetricResult
from evidently.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, expected_result",
    (
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n", "n", "d"]}),
            None,
            ColumnDistributionMetric(column_name="category_feature"),
            ColumnDistributionMetricResult(
                column_name="category_feature",
                current={"n": 3, "d": 2, "p": 1},
                reference=None,
            ),
        ),
    ),
)
def test_column_distribution_metric_success(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnDistributionMetric,
    expected_result: ColumnDistributionMetricResult,
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
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            ColumnDistributionMetric(column_name="feature"),
            "Column 'feature' was not found in current data.",
        ),
        (
            pd.DataFrame({"feature": [0, 2, 2, 432]}),
            pd.DataFrame({"num_feature": [0, 2, 2, 432]}),
            ColumnDistributionMetric(column_name="feature"),
            "Column 'feature' was not found in reference data.",
        ),
    ),
)
def test_column_distribution_metric_value_error(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnDistributionMetric,
    error_message: str,
) -> None:
    with pytest.raises(ValueError) as error:
        metric.calculate(
            data=InputData(
                current_data=current_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping()
            )
        )

    assert error.value.args[0] == error_message


@pytest.mark.parametrize(
    "current_data, reference_data, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3]}),
            None,
            ColumnDistributionMetric(column_name="col"),
            {"column_name": "col", "current": {"1": 1, "2": 1, "3": 1}, "reference": None},
        ),
        (
            pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, 3.5]}),
            pd.DataFrame(
                {
                    "col1": [10, 20, 3.5],
                    "col2": [1, 2, 3],
                }
            ),
            ColumnDistributionMetric(column_name="col1"),
            {"column_name": "col1", "current": {"1": 1, "2": 1, "3": 1}, "reference": {"10.0": 1, "20.0": 1, "3.5": 1}},
        ),
    ),
)
def test_column_distribution_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnDistributionMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnDistributionMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnDistributionMetric"] == expected_json
