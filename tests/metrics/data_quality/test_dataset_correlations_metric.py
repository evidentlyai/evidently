import json

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import DatasetCorrelationsMetric
from evidently.metrics.base_metric import InputData
from evidently.report import Report


def test_dataset_correlation_metric_success() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature_1": [0, 2, 2, 2, 0],
            "numerical_feature_2": [0, 2, 2, 2, 0],
            "category_feature": [1, 2, 4, 2, 1],
            "target": [0, 2, 2, 2, 0],
            "prediction": [0, 2, 2, 2, 0],
        }
    )
    data_mapping = ColumnMapping()
    metric = DatasetCorrelationsMetric()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=None, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.current.target_prediction_correlation == 1.0
    assert result.current.abs_max_target_features_correlation == 1.0
    assert result.current.abs_max_prediction_features_correlation == 1.0
    assert result.current.abs_max_correlation == 1.0
    assert result.current.abs_max_num_features_correlation == 1.0
    assert result.reference is None


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, metric, expected_json",
    (
        (
            pd.DataFrame({"col": [1, 2, 3] * 1000}),
            None,
            ColumnMapping(),
            DatasetCorrelationsMetric(),
            {
                "current": {
                    "abs_max_correlation": 0.0,
                    "abs_max_num_features_correlation": 0.0,
                    "abs_max_prediction_features_correlation": None,
                    "abs_max_target_features_correlation": None,
                    "target_prediction_correlation": None,
                },
                "reference": None,
            },
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
            DatasetCorrelationsMetric(),
            {
                "current": {
                    "abs_max_correlation": 0.0,
                    "abs_max_num_features_correlation": 0.0,
                    "abs_max_prediction_features_correlation": 1.0,
                    "abs_max_target_features_correlation": 1.0,
                    "target_prediction_correlation": None,
                },
                "reference": {
                    "abs_max_correlation": 0.0,
                    "abs_max_num_features_correlation": 0.0,
                    "abs_max_prediction_features_correlation": 0.0,
                    "abs_max_target_features_correlation": 1.0,
                    "target_prediction_correlation": 0.0,
                },
            },
        ),
    ),
)
def test_dataset_correlations_metric_with_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    metric: DatasetCorrelationsMetric,
    expected_json: dict,
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "DatasetCorrelationsMetric" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["DatasetCorrelationsMetric"] == expected_json
