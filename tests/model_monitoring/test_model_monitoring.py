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
    reference_data = pd.DataFrame({
        'target': [1, 2, 3, 4, 5],
        'prediction': [1, 2, 7, 2, 1],
        'numerical_feature_1': [0.5, 0.0, 4.8, 2.1, 4.2],
        'numerical_feature_2': [0, 5, 6, 3, 6],
        'categorical_feature_1': [1, 1, 0, 1, 0],
        'categorical_feature_2': [0, 1, 0, 0, 0],
    })
    current_data = pd.DataFrame({
        'target': [5, 4, 3, 2, 1],
        'prediction': [1, 7, 2, 7, 1],
        'numerical_feature_1': [0.6, 0.1, 45.3, 2.6, 4.2],
        'numerical_feature_2': [0, 5, 3, 7, 6],
        'categorical_feature_1': [1, 0, 1, 1, 0],
        'categorical_feature_2': [0, 1, 0, 1, 1],
    })
    mapping = column_mapping.ColumnMapping(
        categorical_features=['categorical_feature_1', 'categorical_feature_2'],
        numerical_features=['numerical_feature_1', 'numerical_feature_2']
    )
    evidently_monitoring = model_monitoring.ModelMonitoring(
        monitors=[
            model_monitoring.CatTargetDriftMonitor(),
            model_monitoring.NumTargetDriftMonitor(),
            model_monitoring.DataDriftMonitor(),
            model_monitoring.RegressionPerformanceMonitor(),
            model_monitoring.ClassificationPerformanceMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(reference_data=reference_data, current_data=current_data, column_mapping=mapping)
    result = _collect_metrics_results(evidently_monitoring.metrics())

    assert 'cat_target_drift:count' in result
    assert 'cat_target_drift:drift' in result
    assert 'num_target_drift:count' in result
    assert 'num_target_drift:drift' in result
    assert 'num_target_drift:current_correlations' in result
    assert 'num_target_drift:reference_correlations' in result
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


def test_model_monitoring_with_classified_data() -> None:
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


def test_classification_monitoring_metrics() -> None:
    reference_data = pd.DataFrame({
        'target': [1, 0, 1, 0],
        'prediction': [1, 1, 0, 1],
    })
    current_data = pd.DataFrame({
        'target': [0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        'prediction': [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    })
    evidently_monitoring = model_monitoring.ModelMonitoring(
        monitors=[
            model_monitoring.ClassificationPerformanceMonitor(),
        ],
        options=None,
    )
    evidently_monitoring.execute(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping.ColumnMapping(),
    )
    result = _collect_metrics_results(evidently_monitoring.metrics())
    assert 'classification_performance:quality' in result
    assert 'classification_performance:class_quality' in result
    assert 'classification_performance:class_representation' in result
    assert 'classification_performance:confusion' in result
    quality_signals = result['classification_performance:quality']
    assert quality_signals == [
        {'labels': {'dataset': 'reference', 'metric': 'accuracy'}, 'value': 0.25},
        {'labels': {'dataset': 'reference', 'metric': 'precision'}, 'value': 0.16666666666666666},
        {'labels': {'dataset': 'reference', 'metric': 'recall'}, 'value': 0.25},
        {'labels': {'dataset': 'reference', 'metric': 'f1'}, 'value': 0.2},
        {'labels': {'dataset': 'current', 'metric': 'accuracy'}, 'value': 0.2},
        {'labels': {'dataset': 'current', 'metric': 'precision'}, 'value': 0.20833333333333331},
        {'labels': {'dataset': 'current', 'metric': 'recall'}, 'value': 0.20833333333333331},
        {'labels': {'dataset': 'current', 'metric': 'f1'}, 'value': 0.2},
    ]
    class_quality_signals = result['classification_performance:class_quality']
    assert class_quality_signals == [
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'precision'}, 'value': 0.0},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'recall'}, 'value': 0.0},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'f1'}, 'value': 0.0},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'precision'}, 'value': 0.3333333333333333},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'recall'}, 'value': 0.5},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'f1'}, 'value': 0.4},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'precision'}, 'value': 0.16666666666666666},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'recall'}, 'value': 0.25},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'f1'}, 'value': 0.2},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'precision'}, 'value': 0.25},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'recall'}, 'value': 0.16666666666666666},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'f1'}, 'value': 0.2},
    ]
    class_representation_signals = result['classification_performance:class_representation']
    assert class_representation_signals == [
        {'labels': {'class_name': '0', 'dataset': 'reference', 'type': 'target'}, 'value': 2},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'type': 'prediction'}, 'value': 1},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'type': 'target'}, 'value': 2},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'type': 'prediction'}, 'value': 3},
        {'labels': {'class_name': '0', 'dataset': 'current', 'type': 'target'}, 'value': 4},
        {'labels': {'class_name': '0', 'dataset': 'current', 'type': 'prediction'}, 'value': 6},
        {'labels': {'class_name': '1', 'dataset': 'current', 'type': 'target'}, 'value': 6},
        {'labels': {'class_name': '1', 'dataset': 'current', 'type': 'prediction'}, 'value': 4},
    ]

    confusion_signals = result['classification_performance:confusion']
    assert confusion_signals == [
        {'labels': {'class_x_name': '0', 'class_y_name': '0', 'dataset': 'reference'}, 'value': 0},
        {'labels': {'class_x_name': '0', 'class_y_name': '1', 'dataset': 'reference'}, 'value': 2},
        {'labels': {'class_x_name': '1', 'class_y_name': '0', 'dataset': 'reference'}, 'value': 1},
        {'labels': {'class_x_name': '1', 'class_y_name': '1', 'dataset': 'reference'}, 'value': 1},
        {'labels': {'class_x_name': '0', 'class_y_name': '0', 'dataset': 'current'}, 'value': 1},
        {'labels': {'class_x_name': '0', 'class_y_name': '1', 'dataset': 'current'}, 'value': 3},
        {'labels': {'class_x_name': '1', 'class_y_name': '0', 'dataset': 'current'}, 'value': 5},
        {'labels': {'class_x_name': '1', 'class_y_name': '1', 'dataset': 'current'}, 'value': 1},
    ]
    class_confusion_signals = result['classification_performance:class_confusion']
    assert class_confusion_signals == [
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'TP'}, 'value': 0},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'FP'}, 'value': 1},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'TN'}, 'value': 1},
        {'labels': {'class_name': '0', 'dataset': 'reference', 'metric': 'FN'}, 'value': 2},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'TP'}, 'value': 1},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'FP'}, 'value': 2},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'TN'}, 'value': 0},
        {'labels': {'class_name': '1', 'dataset': 'reference', 'metric': 'FN'}, 'value': 1},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'TP'}, 'value': 1},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'FP'}, 'value': 5},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'TN'}, 'value': 1},
        {'labels': {'class_name': '0', 'dataset': 'current', 'metric': 'FN'}, 'value': 3},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'TP'}, 'value': 1},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'FP'}, 'value': 3},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'TN'}, 'value': 1},
        {'labels': {'class_name': '1', 'dataset': 'current', 'metric': 'FN'}, 'value': 5},
    ]
