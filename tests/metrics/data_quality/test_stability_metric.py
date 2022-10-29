import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DataQualityStabilityMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_quality.stability_metric import DataQualityStabilityMetricResult
from evidently.report import Report


@pytest.mark.parametrize(
    "current, reference, metric, expected",
    (
        (
            pd.DataFrame(
                {
                    "numerical_feature_1": [0, 2, 2, 2, 0],
                    "numerical_feature_2": [0, 2, 2, 2, 0],
                    "category_feature": [1, 2, 4, 2, 1],
                    "target": [0, 2, 2, 2, 0],
                    "prediction": [0, 2, 2, 2, 0],
                }
            ),
            None,
            DataQualityStabilityMetric(),
            DataQualityStabilityMetricResult(number_not_stable_target=0, number_not_stable_prediction=0),
        ),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1, 2, 2, 5],
                    "feature2": [1, 1, 2, 2, 8],
                    "target": [1, 0, 1, 1, 0],
                    "prediction": [1, 0, 1, 0, 0],
                }
            ),
            pd.DataFrame(
                {
                    "feature1": [1, 1, 2, 2, 5],
                    "feature2": [1, 1, 2, 2, 8],
                    "target": [1, 0, 1, 1, 0],
                    "prediction": [1, 0, 1, 0, 0],
                }
            ),
            DataQualityStabilityMetric(),
            DataQualityStabilityMetricResult(number_not_stable_target=2, number_not_stable_prediction=4),
        ),
    ),
)
def test_data_quality_stability_metric_success(
    current: pd.DataFrame,
    reference: Optional[pd.DataFrame],
    metric: DataQualityStabilityMetric,
    expected: DataQualityStabilityMetricResult,
) -> None:
    result = metric.calculate(
        data=InputData(current_data=current, reference_data=reference, column_mapping=ColumnMapping())
    )
    assert result == expected


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3] * 1000}),
            None,
            ColumnMapping(),
            DataQualityStabilityMetric(),
            {"number_not_stable_prediction": None, "number_not_stable_target": None},
        ),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1, 2, 2, 5],
                    "feature2": [1, 1, 2, 2, 8],
                    "my_target": [1, 0, 1, 1, 0],
                    "prediction": [1, 0, 1, 0, 0],
                }
            ),
            None,
            ColumnMapping(target="my_target"),
            DataQualityStabilityMetric(),
            {"number_not_stable_prediction": 4, "number_not_stable_target": 2},
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, np.NaN, 3] * 1000,
                    "my_prediction": [1, 2, np.NaN] * 1000,
                    "feature_1": [1, 2, 3] * 1000,
                    "feature_2": ["a", np.NaN, "a"] * 1000,
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, 2, 3] * 10000,
                    "my_prediction": [1, 2, 1] * 10000,
                    "feature_1": [1, 2, 3] * 10000,
                    "feature_2": ["a", "a", "a"] * 10000,
                }
            ),
            ColumnMapping(target="my_target", prediction="my_prediction"),
            DataQualityStabilityMetric(),
            {"number_not_stable_prediction": 0, "number_not_stable_target": 0},
        ),
    ),
)
def test_data_quality_stability_metric_with_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: DataQualityStabilityMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "DataQualityStabilityMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["DataQualityStabilityMetric"] == expected_json
