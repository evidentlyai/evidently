import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently import ColumnMapping
from evidently.calculations.data_quality import ColumnCorrelations
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetricResult
from evidently.report import Report
from evidently.utils.visualizations import Distribution


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, column_mapping, metric, expected_result",
    (
        (
            pd.DataFrame({"category_feature": []}),
            None,
            ColumnMapping(),
            ColumnCorrelationsMetric(column_name="category_feature"),
            ColumnCorrelationsMetricResult(
                column_name="category_feature",
                current={},
                reference=None,
            ),
        ),
        (
            pd.DataFrame(
                {"feature1": ["n", "d", "p", "n"], "feature2": [0, 2, 2, 432], "feature3": ["f", "f", np.NaN, 432]}
            ),
            None,
            ColumnMapping(categorical_features=["feature1", "feature2", "feature3"]),
            ColumnCorrelationsMetric(column_name="feature1"),
            ColumnCorrelationsMetricResult(
                column_name="feature1",
                current={
                    "cramer_v": ColumnCorrelations(
                        column_name="feature1",
                        kind="cramer_v",
                        values=Distribution(x=["feature2", "feature3"], y=[approx(0.7, abs=0.1), 0.5]),
                    )
                },
                reference=None,
            ),
        ),
    ),
)
def test_column_correlations_metric_success(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    column_mapping: ColumnMapping,
    metric: ColumnCorrelationsMetric,
    expected_result: ColumnCorrelationsMetricResult,
) -> None:
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=column_mapping)
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, error_message",
    (
        (
            pd.DataFrame(
                {
                    "feature": [
                        pd.Timestamp("2018-01-05"),
                        pd.Timestamp("2018-01-05"),
                    ]
                }
            ),
            None,
            ColumnCorrelationsMetric(column_name="feature"),
            "Cannot calculate correlations for 'datetime' column type.",
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 2, 2, 432]}),
            None,
            ColumnCorrelationsMetric(column_name="feature"),
            "Column 'feature' was not found in current data.",
        ),
        (
            pd.DataFrame({"feature": [0, 2, 2, 432]}),
            pd.DataFrame({"num_feature": [0, 2, 2, 432]}),
            ColumnCorrelationsMetric(column_name="feature"),
            "Column 'feature' was not found in reference data.",
        ),
    ),
)
def test_column_correlations_metric_value_error(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: ColumnCorrelationsMetric,
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
            pd.DataFrame({"col": [1.4, 2.3, 3.4], "test": ["a", "b", "c"], "test2": ["a", "b", "c"]}),
            None,
            ColumnCorrelationsMetric(column_name="col"),
            {
                "column_name": "col",
                "current": {},
                "reference": None,
            },
        ),
        (
            pd.DataFrame({"col": ["a", "b", "c"], "test": [1.4, 2.3, 3.4], "test2": [1.4, 2.3, 3.4]}),
            None,
            ColumnCorrelationsMetric(column_name="col"),
            {
                "column_name": "col",
                "current": {},
                "reference": None,
            },
        ),
        (
            pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, 3.5]}),
            pd.DataFrame(
                {
                    "col1": [10, 20, 3.5],
                    "col2": [1, 1, 3],
                }
            ),
            ColumnCorrelationsMetric(column_name="col1"),
            {
                "column_name": "col1",
                "current": {
                    "kendall": {
                        "column_name": "col1",
                        "kind": "kendall",
                        "values": {"x": ["col2"], "y": [approx(-0.33, abs=0.01)]},
                    },
                    "pearson": {
                        "column_name": "col1",
                        "kind": "pearson",
                        "values": {"x": ["col2"], "y": [approx(-0.39, abs=0.01)]},
                    },
                    "spearman": {"column_name": "col1", "kind": "spearman", "values": {"x": ["col2"], "y": [-0.5]}},
                },
                "reference": {
                    "kendall": {
                        "column_name": "col1",
                        "kind": "kendall",
                        "values": {"x": ["col2"], "y": [approx(-0.81, abs=0.01)]},
                    },
                    "pearson": {
                        "column_name": "col1",
                        "kind": "pearson",
                        "values": {"x": ["col2"], "y": [approx(-0.79, abs=0.01)]},
                    },
                    "spearman": {
                        "column_name": "col1",
                        "kind": "spearman",
                        "values": {"x": ["col2"], "y": [approx(-0.86, abs=0.01)]},
                    },
                },
            },
        ),
    ),
)
def test_column_correlations_metric_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: ColumnCorrelationsMetric, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "ColumnCorrelationsMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["ColumnCorrelationsMetric"] == expected_json
