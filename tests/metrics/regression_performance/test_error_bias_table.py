import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import RegressionErrorBiasTable
from evidently.metrics.base_metric import InputData
from evidently.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, metric, error_message",
    (
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(),
            "Target column should be present.",
        ),
        (
            pd.DataFrame({"target": [1, 2, 3]}),
            pd.DataFrame({"target": [1, 2, 3]}),
            RegressionErrorBiasTable(columns=["test"]),
            "Prediction column should be present.",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"], "target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(columns=["category_feature"], top=1),
            "Cannot calculate error bias - top should be in range (0, 1).",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"], "target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(columns=["category_feature"], top=5),
            "Cannot calculate error bias - top should be in range (0, 1).",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"], "target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(columns=["category_feature"], top=0),
            "Cannot calculate error bias - top should be in range (0, 1).",
        ),
    ),
)
def test_regression_error_bias_table_value_errors(
    current_dataset: pd.DataFrame,
    reference_dataset: Optional[pd.DataFrame],
    metric: RegressionErrorBiasTable,
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
            pd.DataFrame({"target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(),
            {
                "cat_feature_names": [],
                "columns": ["prediction", "target"],
                "error_bias": {},
                "num_feature_names": [],
                "prediction_name": "prediction",
                "target_name": "target",
            },
        ),
        (
            pd.DataFrame({"target": [1, np.NaN, 3], "prediction": [1, 2, 3], "feature": [np.NaN, "a", np.NaN]}),
            pd.DataFrame(
                {
                    "target": [10, 20, 3.5],
                    "prediction": [1, 2, 3],
                    "feature": ["a", "b", "a"],
                }
            ),
            RegressionErrorBiasTable(),
            {
                "cat_feature_names": ["feature"],
                "columns": ["feature", "prediction", "target"],
                "error_bias": {
                    "feature": {
                        "current_majority": None,
                        "current_over": None,
                        "current_range": 1.0,
                        "current_under": None,
                        "feature_type": "cat",
                        "ref_majority": "a",
                        "ref_over": "a",
                        "ref_range": 1.0,
                        "ref_under": "b",
                    }
                },
                "num_feature_names": [],
                "prediction_name": "prediction",
                "target_name": "target",
            },
        ),
    ),
)
def test_regression_error_bias_table_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: RegressionErrorBiasTable, expected_json: dict
) -> None:
    report = Report(metrics=[metric])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    json_result = report.json()
    assert len(json_result) > 0
    parsed_json_result = json.loads(json_result)
    assert "metrics" in parsed_json_result
    assert "RegressionErrorBiasTable" in parsed_json_result["metrics"]
    assert json.loads(json_result)["metrics"]["RegressionErrorBiasTable"] == expected_json
