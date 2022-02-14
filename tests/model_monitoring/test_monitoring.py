"""Test common-cases with different dataset types and a few monitors"""

import pandas as pd

import pytest

from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring import DataDriftMonitor
from evidently.model_monitoring import CatTargetDriftMonitor
from evidently.model_monitoring import NumTargetDriftMonitor
from evidently.model_monitoring import RegressionPerformanceMonitor
from evidently.model_monitoring import ClassificationPerformanceMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric
from evidently.pipeline.column_mapping import ColumnMapping

from tests.model_monitoring.helpers import collect_metrics_results


def test_model_monitoring_with_simple_data():
    reference_data = pd.DataFrame(
        {
            "target": [1, 2, 3, 4, 5],
            "prediction": [1, 2, 7, 2, 1],
            "numerical_feature_1": [0.5, 0.0, 4.8, 2.1, 4.2],
            "numerical_feature_2": [0, 5, 6, 3, 6],
            "categorical_feature_1": [1, 1, 0, 1, 0],
            "categorical_feature_2": [0, 1, 0, 0, 0],
        }
    )
    current_data = pd.DataFrame(
        {
            "target": [5, 4, 3, 2, 1],
            "prediction": [1, 7, 2, 7, 1],
            "numerical_feature_1": [0.6, 0.1, 45.3, 2.6, 4.2],
            "numerical_feature_2": [0, 5, 3, 7, 6],
            "categorical_feature_1": [1, 0, 1, 1, 0],
            "categorical_feature_2": [0, 1, 0, 1, 1],
        }
    )
    mapping = ColumnMapping(
        categorical_features=["categorical_feature_1", "categorical_feature_2"],
        numerical_features=["numerical_feature_1", "numerical_feature_2"],
    )
    evidently_monitoring = ModelMonitoring(
        monitors=[
            CatTargetDriftMonitor(),
            NumTargetDriftMonitor(),
            DataDriftMonitor(),
            RegressionPerformanceMonitor(),
            ClassificationPerformanceMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(reference_data=reference_data, current_data=current_data, column_mapping=mapping)
    result = collect_metrics_results(evidently_monitoring.metrics())

    assert "cat_target_drift:count" in result
    assert "cat_target_drift:drift" in result
    assert "num_target_drift:count" in result
    assert "num_target_drift:drift" in result
    assert "num_target_drift:current_correlations" in result
    assert "num_target_drift:reference_correlations" in result
    assert "data_drift:dataset_drift" in result
    assert "data_drift:n_drifted_features" in result
    assert "data_drift:p_value" in result
    assert "data_drift:share_drifted_features" in result
    assert "regression_performance:error_normality" in result
    assert "regression_performance:feature_error_bias" in result
    assert "regression_performance:quality" in result
    assert "regression_performance:underperformance" in result
    assert "classification_performance:quality" in result
    assert "classification_performance:class_representation" in result
    assert "classification_performance:class_quality" in result
    assert "classification_performance:confusion" in result


def test_metric_creation_with_incorrect_labels():
    metric = ModelMonitoringMetric("test_metric", ["option_1"])
    metric.create(123, {"option_1": "value"})

    with pytest.raises(ValueError):
        metric.create(123)

    with pytest.raises(ValueError):
        metric.create(123, {"option_2": "value"})

    with pytest.raises(ValueError):
        metric.create(123, {"option_1": "value", "option_2": "value"})
