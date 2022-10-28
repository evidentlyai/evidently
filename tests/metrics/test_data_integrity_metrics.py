import numpy as np
import pandas as pd

from evidently.metrics import DataIntegrityMetrics
from evidently.metrics.base_metric import InputData
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


def test_data_integrity_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.NAN, 1],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataIntegrityMetrics()
    result = metric.calculate(
        data=InputData(
            current_data=test_dataset, reference_data=None, column_mapping=data_mapping
        )
    )
    assert result is not None
    assert result.current.number_of_columns == 4
    assert result.current.number_of_rows == 3


def test_dataset_missing_values_metrics_with_report() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature": [" a", "a", "\tb", np.nan, np.nan],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[DataIntegrityMetrics()])
    report.run(
        current_data=test_dataset, reference_data=None, column_mapping=data_mapping
    )
    assert report.show()
    assert report.json()

    report.run(
        current_data=test_dataset,
        reference_data=test_dataset,
        column_mapping=data_mapping,
    )
    assert report.show()
    assert report.json()
