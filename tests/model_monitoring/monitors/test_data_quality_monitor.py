from datetime import datetime

import pandas as pd

from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring.monitors.data_quality import DataQualityMonitor
from evidently.pipeline.column_mapping import ColumnMapping

from tests.model_monitoring.helpers import collect_metrics_results


def test_monitor_id():
    assert DataQualityMonitor().monitor_id() == "data_quality"


def test_data_quality_monitor_regression() -> None:
    reference_data = pd.DataFrame(
        {
            "my_target": [1, 2, 1, 4],
            "my_prediction": [2, -1, 1, -1],
            "numerical_feature": [0, 2, -1, 5],
            "categorical_feature": ["y", "y", "n", "u"],
            "datetime_feature": [
                datetime(year=2012, month=1, day=5),
                datetime(year=2002, month=12, day=5),
                datetime(year=2012, month=1, day=5),
                datetime(year=2012, month=1, day=6),
            ],
        }
    )
    current_data = pd.DataFrame(
        {
            "my_target": [1],
            "my_prediction": [0],
            "numerical_feature": [5],
            "categorical_feature": ["y"],
            "datetime_feature": [datetime(year=2012, month=1, day=5)],
        }
    )
    data_mapping = ColumnMapping(
        target="my_target",
        prediction="my_prediction",
        numerical_features=["numerical_feature"],
        categorical_features=["categorical_feature"],
        datetime_features=["datetime_feature"],
        task="regression",
    )
    evidently_monitoring = ModelMonitoring(monitors=[DataQualityMonitor()], options=None)
    evidently_monitoring.execute(reference_data=reference_data, current_data=current_data, column_mapping=data_mapping)
    result = collect_metrics_results(evidently_monitoring.metrics())
    assert "data_quality:quality_stat" in result
    assert result["data_quality:quality_stat"] == [
        {"labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "count"},
         "value": 4},
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "infinite_count"},
            "value": 0,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "my_target",
                "feature_type": "num",
                "metric": "infinite_percentage",
            },
            "value": 0.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "unique_count"},
            "value": 3,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "unique_percentage"},
            "value": 75.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "percentile_25"},
            "value": 1.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "percentile_50"},
            "value": 1.5,
        },
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "percentile_75"},
            "value": 2.5,
        },
        {"labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "max"},
         "value": 4},
        {"labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "min"},
         "value": 1},
        {"labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "mean"},
         "value": 2.0},
        {
            "labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num",
                       "metric": "most_common_value"},
            "value": 1,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "my_target",
                "feature_type": "num",
                "metric": "most_common_value_percentage",
            },
            "value": 50.0,
        },
        {"labels": {"dataset": "reference", "feature": "my_target", "feature_type": "num", "metric": "std"},
         "value": 1.41},
        {
            "labels": {"dataset": "reference", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "count"},
            "value": 4,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "missing_count",
            },
            "value": 0,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "missing_percentage",
            },
            "value": 0.0,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "unique_count",
            },
            "value": 3,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "unique_percentage",
            },
            "value": 75.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "max"},
            "value": "2012-01-06 00:00:00",
        },
        {
            "labels": {"dataset": "reference", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "min"},
            "value": "2002-12-05 00:00:00",
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "most_common_value",
            },
            "value": "2012-01-05 00:00:00",
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "most_common_value_percentage",
            },
            "value": 50.0,
        },
        {"labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat", "metric": "count"},
         "value": 4},
        {
            "labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "unique_count"},
            "value": 3,
        },
        {
            "labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "unique_percentage"},
            "value": 75.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "most_common_value"},
            "value": "y",
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "categorical_feature",
                "feature_type": "cat",
                "metric": "most_common_value_percentage",
            },
            "value": 50.0,
        },
        {"labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num", "metric": "count"},
         "value": 4},
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "infinite_count"},
            "value": 0,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "numerical_feature",
                "feature_type": "num",
                "metric": "infinite_percentage",
            },
            "value": 0.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "unique_count"},
            "value": 4,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "unique_percentage"},
            "value": 100.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_25"},
            "value": -0.25,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_50"},
            "value": 1.0,
        },
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_75"},
            "value": 2.75,
        },
        {"labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num", "metric": "max"},
         "value": 5},
        {"labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num", "metric": "min"},
         "value": -1},
        {"labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num", "metric": "mean"},
         "value": 1.5},
        {
            "labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "most_common_value"},
            "value": 5,
        },
        {
            "labels": {
                "dataset": "reference",
                "feature": "numerical_feature",
                "feature_type": "num",
                "metric": "most_common_value_percentage",
            },
            "value": 25.0,
        },
        {"labels": {"dataset": "reference", "feature": "numerical_feature", "feature_type": "num", "metric": "std"},
         "value": 2.65},
        {"labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "count"},
         "value": 1},
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "infinite_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num",
                       "metric": "infinite_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "unique_count"},
            "value": 1,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num",
                       "metric": "unique_percentage"},
            "value": 100.0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "percentile_25"},
            "value": 1.0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "percentile_50"},
            "value": 1.0,
        },
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "percentile_75"},
            "value": 1.0,
        },
        {"labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "max"}, "value": 1},
        {"labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "min"}, "value": 1},
        {"labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "mean"},
         "value": 1.0},
        {
            "labels": {"dataset": "current", "feature": "my_target", "feature_type": "num",
                       "metric": "most_common_value"},
            "value": 1,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "my_target",
                "feature_type": "num",
                "metric": "most_common_value_percentage",
            },
            "value": 100.0,
        },
        {"labels": {"dataset": "current", "feature": "my_target", "feature_type": "num", "metric": "std"},
         "value": None},
        {
            "labels": {"dataset": "current", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "count"},
            "value": 1,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "missing_count",
            },
            "value": 0,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "missing_percentage",
            },
            "value": 0.0,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "unique_count",
            },
            "value": 1,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "unique_percentage",
            },
            "value": 100.0,
        },
        {
            "labels": {"dataset": "current", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "max"},
            "value": "2012-01-05 00:00:00",
        },
        {
            "labels": {"dataset": "current", "feature": "datetime_feature", "feature_type": "datetime",
                       "metric": "min"},
            "value": "2012-01-05 00:00:00",
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "most_common_value",
            },
            "value": "2012-01-05 00:00:00",
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "datetime_feature",
                "feature_type": "datetime",
                "metric": "most_common_value_percentage",
            },
            "value": 100.0,
        },
        {"labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat", "metric": "count"},
         "value": 1},
        {
            "labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "unique_count"},
            "value": 1,
        },
        {
            "labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "unique_percentage"},
            "value": 100.0,
        },
        {
            "labels": {"dataset": "current", "feature": "categorical_feature", "feature_type": "cat",
                       "metric": "most_common_value"},
            "value": "y",
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "categorical_feature",
                "feature_type": "cat",
                "metric": "most_common_value_percentage",
            },
            "value": 100.0,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "categorical_feature",
                "feature_type": "cat",
                "metric": "new_in_current_values_count",
            },
            "value": 0,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "categorical_feature",
                "feature_type": "cat",
                "metric": "unused_in_current_values_count",
            },
            "value": 2,
        },
        {"labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num", "metric": "count"},
         "value": 1},
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "infinite_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "infinite_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "missing_count"},
            "value": 0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "missing_percentage"},
            "value": 0.0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "unique_count"},
            "value": 1,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "unique_percentage"},
            "value": 100.0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_25"},
            "value": 5.0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_50"},
            "value": 5.0,
        },
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "percentile_75"},
            "value": 5.0,
        },
        {"labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num", "metric": "max"},
         "value": 5},
        {"labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num", "metric": "min"},
         "value": 5},
        {"labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num", "metric": "mean"},
         "value": 5.0},
        {
            "labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num",
                       "metric": "most_common_value"},
            "value": 5,
        },
        {
            "labels": {
                "dataset": "current",
                "feature": "numerical_feature",
                "feature_type": "num",
                "metric": "most_common_value_percentage",
            },
            "value": 100.0,
        },
        {"labels": {"dataset": "current", "feature": "numerical_feature", "feature_type": "num", "metric": "std"},
         "value": None},
    ]
