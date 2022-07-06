import numpy as np
import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_drift_metrics import DataDriftMetrics


def test_data_drift_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.NAN, 1],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    metric = DataDriftMetrics()
    result = metric.calculate(
        data=InputData(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping), metrics={}
    )
    assert result is not None
    assert result.analyzer_result.metrics.n_drifted_features == 0
