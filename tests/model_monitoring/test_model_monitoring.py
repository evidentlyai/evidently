from collections import defaultdict
from typing import Dict
from typing import Generator
from typing import List

import pandas as pd

from evidently import model_monitoring
from evidently.model_monitoring import monitoring
from evidently.pipeline import column_mapping


def _collect_metrics_results(metrics: Generator[monitoring.MetricsType, None, None]) -> Dict[str, List]:
    result = defaultdict(list)

    for metric, value, labels in metrics:
        result[metric.name].append({
            'value': value,
            'labels': labels,
        })
    return result


def test_model_monitoring_with_simple_data():
    test_data = pd.DataFrame({
        'target': [1, 2, 3, 4, 5],
        'prediction': [5, 4, 3, 2, 1],
        'numerical_feature_1': [0.5, 0.0, 4.8, 2.1, 4.2],
        'numerical_feature_2': [0, 5, 6, 3, 6],
        'categorical_feature_1': [1, 1, 0, 1, 0],
        'categorical_feature_2': [0, 1, 0, 0, 0],
    })
    mapping = column_mapping.ColumnMapping(
        categorical_features=['categorical_feature_1', 'categorical_feature_2'],
        numerical_features=['numerical_feature_1', 'numerical_feature_2']
    )
    evidently_monitoring = model_monitoring.ModelMonitoring(
        monitors=[
            model_monitoring.DataDriftMonitor(),
            model_monitoring.RegressionPerformanceMonitor(),
            model_monitoring.ClassificationPerformanceMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(test_data, test_data, column_mapping=mapping)
    result = _collect_metrics_results(evidently_monitoring.metrics())

    assert 'data_drift:dataset_drift' in result
    assert 'data_drift:n_drifted_features' in result
    assert 'data_drift:p_value' in result
    assert 'data_drift:share_drifted_features' in result
    assert 'regression_performance:error_normality' in result
    assert 'regression_performance:feature_error_bias' in result
    assert 'regression_performance:quality' in result
    assert 'regression_performance:underperformance' in result
    assert 'classification_performance:quality' in result
    assert 'classification_performance:class_representation' in result
    assert 'classification_performance:class_quality' in result
    assert 'classification_performance:confusion' in result


def test_model_monitoring_with_classified_data():
    reference_data = pd.DataFrame(
        {
            'target': ['label_a', 'label_a', 'label_b', 'label_b', 'label_c', 'label_c'],
            'label_a': [.1, .2, .3, .4, .4, .1],
            'label_b': [.3, .1, .7, .5, .5, .1],
            'label_c': [.7, .8, .0, .1, .1, .8],
        }
    )
    mapping = column_mapping.ColumnMapping(
        target='target',
        prediction=['label_a', 'label_c', 'label_b'],
    )
    evidently_monitoring = model_monitoring.ModelMonitoring(
        monitors=[
            model_monitoring.ProbClassificationPerformanceMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(reference_data, None, column_mapping=mapping)
    result = _collect_metrics_results(evidently_monitoring.metrics())

    assert 'prob_classification_performance:quality' in result
