import numpy as np
import pandas as pd

from evidently.legacy.metrics import RegressionPerformanceMetrics
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.report import Report


def test_regression_performance_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [1, 2, 3],
            "prediction": [1, np.nan, 1],
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


def test_regression_performance_metrics_current_data_differ_from_reference() -> None:
    reference_data = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3", "4"],
            "numerical_feature": [3, 2, 1, 0],
            "my_target": [1, 2, 3, 4],
            "my_prediction": [4, 3, 2, 1],
        }
    )
    current_data = pd.DataFrame(
        {
            "category_feature": ["5"],
            "another_numerical_feature": [10],
            "my_target": [6],
            "my_prediction": [7],
        }
    )
    data_mapping = ColumnMapping(target="my_target", prediction="my_prediction")

    report = Report(metrics=[RegressionPerformanceMetrics()])
    report.run(current_data=current_data, reference_data=reference_data, column_mapping=data_mapping)
    assert report.show()
    assert report.json()
