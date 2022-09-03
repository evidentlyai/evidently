import numpy as np
import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics import RegressionPerformanceMetrics
from evidently.report import Report


def test_regression_performance_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [1, 2, 3],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()

    report = Report(metrics=[RegressionPerformanceMetrics()])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.metrics is not None
    assert report.show() is not None
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.metrics is not None
    assert report.show() is not None
    assert report.json()
