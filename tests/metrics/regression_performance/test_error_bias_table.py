import json
from typing import Optional

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics import RegressionErrorBiasTable
from evidently.legacy.options.agg_data import RenderOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


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
            RegressionErrorBiasTable(columns=["category_feature"], top_error=0.5),
            "Cannot calculate error bias - top error should be in range (0, 0.5).",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"], "target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(columns=["category_feature"], top_error=5),
            "Cannot calculate error bias - top error should be in range (0, 0.5).",
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c"], "target": [1, 2, 3], "prediction": [1, 2, 3]}),
            None,
            RegressionErrorBiasTable(columns=["category_feature"], top_error=0),
            "Cannot calculate error bias - top error should be in range (0, 0.5).",
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
        report = Report(metrics=[metric], options=Options(render=RenderOptions(raw_data=True)))
        report.run(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
        metric.get_result()

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
                "columns": [],
                "error_bias": {},
                "num_feature_names": [],
                "prediction_name": "prediction",
                "target_name": "target",
                "top_error": 0.05,
            },
        ),
        (
            pd.DataFrame({"target": [1, np.nan, 3], "prediction": [1, 2, 3], "feature": [np.nan, "a", np.nan]}),
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
                "columns": ["feature"],
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
                "top_error": 0.05,
            },
        ),
    ),
)
def test_regression_error_bias_table_with_report(
    current_data: pd.DataFrame, reference_data: pd.DataFrame, metric: RegressionErrorBiasTable, expected_json: dict
) -> None:
    report = Report(metrics=[metric], options=Options(render=RenderOptions(raw_data=True)))
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=ColumnMapping())
    assert report.show()
    result_json = report.json()
    assert len(result_json) > 0
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "RegressionErrorBiasTable"
    assert result["metrics"][0]["result"] == expected_json
