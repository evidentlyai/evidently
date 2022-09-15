"""Test common-cases with different dataset types and a few monitors"""

from typing import ClassVar

import pandas as pd
import pytest

from evidently.model_monitoring import (CatTargetDriftMonitor,
                                        ClassificationPerformanceMonitor,
                                        DataDriftMonitor, DataQualityMonitor,
                                        ModelMonitoring, NumTargetDriftMonitor,
                                        ProbClassificationPerformanceMonitor,
                                        RegressionPerformanceMonitor)
from evidently.model_monitoring.monitoring import (ModelMonitor,
                                                   ModelMonitoringMetric)
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
            DataQualityMonitor(),
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
    assert "data_drift:value" in result
    assert "data_drift:share_drifted_features" in result
    assert "regression_performance:error_normality" in result
    assert "regression_performance:feature_error_bias" in result
    assert "regression_performance:quality" in result
    assert "regression_performance:underperformance" in result
    assert "classification_performance:quality" in result
    assert "classification_performance:class_representation" in result
    assert "classification_performance:class_quality" in result
    assert "classification_performance:confusion" in result
    assert "data_quality:quality_stat" in result


def test_data_drift_monitoring_labels_with_simple_data():
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
            DataDriftMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(reference_data=reference_data, current_data=current_data, column_mapping=mapping)
    result = collect_metrics_results(evidently_monitoring.metrics())

    assert "data_drift:dataset_drift" in result
    assert "data_drift:n_drifted_features" in result
    assert "data_drift:value" in result

    data_drift_value = result["data_drift:value"]
    for e in data_drift_value:
        assert "stat_test" in e["labels"]
        assert "feature" in e["labels"]
        assert "feature_type" in e["labels"]


def test_metric_creation_with_incorrect_labels():
    metric = ModelMonitoringMetric("test_metric", ["option_1"])
    metric.create(123, {"option_1": "value"})

    with pytest.raises(ValueError):
        metric.create(123)

    with pytest.raises(ValueError):
        metric.create(123, {"option_2": "value"})

    with pytest.raises(ValueError):
        metric.create(123, {"option_1": "value", "option_2": "value"})


@pytest.mark.parametrize(
    "monitor_class, raises_value_error",
    (
        (DataQualityMonitor, False),
        (RegressionPerformanceMonitor, False),
        (ClassificationPerformanceMonitor, False),
        (DataDriftMonitor, True),
        (CatTargetDriftMonitor, True),
        (NumTargetDriftMonitor, True),
    ),
)
def test_model_monitoring_without_current_data(monitor_class: ClassVar[ModelMonitor], raises_value_error: bool) -> None:
    """Check that monitors
    - that can be executed with one dataset only do not get an error
    - that cannot be executed with one dataset raise correct error
    """
    test_data = pd.DataFrame(
        {"target": [1, 0, 1], "prediction": [1, 0, 0], "num_feature": [1, 2, 3], "cat_feature": [3, 2, 1]}
    )
    data_mapping = ColumnMapping(numerical_features=["num_feature"], categorical_features=["cat_feature"])
    evidently_monitoring = ModelMonitoring([monitor_class()])

    if raises_value_error:
        with pytest.raises(ValueError) as error:
            evidently_monitoring.execute(test_data, column_mapping=data_mapping)

        assert error.value.args[0] == "current_data should be present"

    else:
        evidently_monitoring.execute(test_data, column_mapping=data_mapping)
        assert evidently_monitoring.analyzers_results is not None

    evidently_monitoring.execute(test_data, test_data, data_mapping)
    assert evidently_monitoring.analyzers_results is not None


def test_model_monitoring_without_current_data_prob_classification() -> None:
    test_data = pd.DataFrame(
        {
            "target": ["0", "1", "0", "1"],
            "0": [0.1, 0.2, 0.3, 0.4],
            "1": [0.5, 0.6, 0.7, 0.8],
        }
    )
    data_mapping = ColumnMapping(
        target="target",
        prediction=["0", "1"],
    )
    evidently_monitoring = ModelMonitoring([ProbClassificationPerformanceMonitor()])

    evidently_monitoring.execute(test_data, column_mapping=data_mapping)
    assert evidently_monitoring.analyzers_results is not None

    evidently_monitoring.execute(test_data, test_data, data_mapping)
    assert evidently_monitoring.analyzers_results is not None
