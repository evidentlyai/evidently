import json
from typing import Optional

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metric_preset import DataQualityPreset
from evidently.report import Report


@pytest.mark.parametrize(
    "current_data, reference_data, column_mapping, expected_json",
    (
        (
            pd.DataFrame(),
            None,
            ColumnMapping(),
            {
                "DatasetCorrelationsMetric": {
                    "current": {
                        "abs_max_correlation": None,
                        "abs_max_num_features_correlation": None,
                        "abs_max_prediction_features_correlation": None,
                        "abs_max_target_features_correlation": None,
                        "num_features": [],
                        "target_prediction_correlation": None,
                    },
                    "reference": None,
                },
                "DatasetMissingValuesMetric": {
                    "columns_with_nulls": [],
                    "different_nulls": {"": 0, "-Infinity": 0, "Infinity": 0, "null": 0},
                    "different_nulls_by_column": {},
                    "number_of_columns": 0,
                    "number_of_columns_with_nulls": 0,
                    "number_of_different_nulls": 0,
                    "number_of_different_nulls_by_column": {},
                    "number_of_missed_values": 0,
                    "number_of_nulls_by_column": {},
                    "number_of_rows": 0,
                    "number_of_rows_with_nulls": 0,
                    "share_of_columns_with_nulls": 0.0,
                    "share_of_missed_values": 0.0,
                    "share_of_nulls_by_column": {},
                    "share_of_rows_with_nulls": 0.0,
                },
            },
        ),
        (
            pd.DataFrame(),
            pd.DataFrame(),
            ColumnMapping(),
            {
                "DatasetCorrelationsMetric": {
                    "current": {
                        "abs_max_correlation": None,
                        "abs_max_num_features_correlation": None,
                        "abs_max_prediction_features_correlation": None,
                        "abs_max_target_features_correlation": None,
                        "num_features": [],
                        "target_prediction_correlation": None,
                    },
                    "reference": {
                        "abs_max_correlation": None,
                        "abs_max_num_features_correlation": None,
                        "abs_max_prediction_features_correlation": None,
                        "abs_max_target_features_correlation": None,
                        "num_features": [],
                        "target_prediction_correlation": None,
                    },
                },
                "DatasetMissingValuesMetric": {
                    "columns_with_nulls": [],
                    "different_nulls": {"": 0, "-Infinity": 0, "Infinity": 0, "null": 0},
                    "different_nulls_by_column": {},
                    "number_of_columns": 0,
                    "number_of_columns_with_nulls": 0,
                    "number_of_different_nulls": 0,
                    "number_of_different_nulls_by_column": {},
                    "number_of_missed_values": 0,
                    "number_of_nulls_by_column": {},
                    "number_of_rows": 0,
                    "number_of_rows_with_nulls": 0,
                    "share_of_columns_with_nulls": 0.0,
                    "share_of_missed_values": 0.0,
                    "share_of_nulls_by_column": {},
                    "share_of_rows_with_nulls": 0.0,
                },
            },
        ),
    ),
)
def test_data_quality_preset(
    current_data: pd.DataFrame, reference_data: Optional[pd.DataFrame], column_mapping, expected_json: dict
) -> None:
    report = Report(metrics=[DataQualityPreset()])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    assert report.show()
    json_result = report.json()
    result = json.loads(json_result)
    assert "metrics" in result
    assert result["metrics"] == expected_json
