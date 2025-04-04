import json

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics import DatasetCorrelationsMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


def test_dataset_correlation_metric_success() -> None:
    current_dataset = pd.DataFrame(
        {
            "numerical_feature_1": [0, 2, 2, 2, 0],
            "numerical_feature_2": [0, 2, 2, 2, 0],
            "category_feature": [1, 2, 4, 2, 1],
            "target": [0.0, 2.0, 2.0, 2.0, 0.0],
            "prediction": [0.0, 2.0, 2.0, 2.0, 0.0],
        }
    )
    data_mapping = ColumnMapping(task="regression")
    metric = DatasetCorrelationsMetric()
    report = Report(metrics=[metric])
    report.run(current_data=current_dataset, reference_data=None, column_mapping=data_mapping)
    result = metric.get_result()
    assert result is not None
    assert result.current is not None
    assert result.current.stats is not None
    assert result.reference is None


@pytest.mark.skip("need fixing in future")
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
                    "stats": {
                        "cramer_v": {
                            "abs_max_correlation": None,
                            "abs_max_features_correlation": None,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "kendall": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "pearson": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "spearman": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                    }
                },
                "reference": None,
            },
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, np.nan, 3] * 1000,
                    "my_prediction": [1, 2, np.nan] * 1000,
                    "feature_1": [1, 2, 3] * 1000,
                    "feature_2": ["a", np.nan, "a"] * 1000,
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
                    "stats": {
                        "cramer_v": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": None,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "kendall": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "pearson": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "spearman": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                    }
                },
                "reference": {
                    "stats": {
                        "cramer_v": {
                            "abs_max_correlation": 0.9999999999999999,
                            "abs_max_features_correlation": None,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": 0.9999999999999999,
                        },
                        "kendall": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "pearson": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                        "spearman": {
                            "abs_max_correlation": 0.0,
                            "abs_max_features_correlation": 0.0,
                            "abs_max_prediction_features_correlation": None,
                            "abs_max_target_features_correlation": None,
                            "target_prediction_correlation": None,
                        },
                    }
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
    result_json = report.json()
    assert len(result_json) > 0
    result = json.loads(result_json)
    assert result["metrics"][0]["metric"] == "DatasetCorrelationsMetric"
    assert result["metrics"][0]["result"] == expected_json
