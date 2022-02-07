from collections import defaultdict

import pandas as pd

from evidently import model_monitoring
from evidently.pipeline import column_mapping


def test_model_monitoring_with_all_monitors():
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
    monitoring = model_monitoring.ModelMonitoring(
        monitors=[
            model_monitoring.DataDriftMonitor(),
            model_monitoring.RegressionPerformanceMonitor()
        ],
        options=[],
    )
    monitoring.execute(test_data, test_data, column_mapping=mapping)
    result = defaultdict(list)

    for metric, value, labels in monitoring.metrics():
        result[metric.name].append({
            'value': value,
            'labels': labels,
        })

    assert 'data_drift:dataset_drift' in result
    assert 'data_drift:n_drifted_features' in result
    assert 'data_drift:p_value' in result
    assert 'data_drift:share_drifted_features' in result
    assert 'regression_performance:error_normality' in result
    assert 'regression_performance:feature_error_bias' in result
    assert 'regression_performance:quality' in result
    assert 'regression_performance:underperformance' in result
