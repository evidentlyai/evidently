import numpy as np
import pandas as pd

from evidently.legacy.metrics import DiversityMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_curr_rank():
    curr = pd.DataFrame(
        {
            "user_id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "item_id": ["0a", "1a", "5a", "6a", "0a", "1a", "5a", "6a", "0a", "4a", "6a", "10a"],
            "item_f1": [1, 1, 1, -0.1, 1, 1, 1, -0.1, 1, 1, -0.1, -1],
            "item_f2": [0, 0.1, 1, 0.9, 0, 0.1, 1, 0.9, 0, 0.9, 0.9, -1],
            "target": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "prediction": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
        }
    )
    metric = DiversityMetric(k=4, item_features=["item_f1", "item_f2"])
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=curr, column_mapping=column_mapping)

    results = metric.get_result()
    assert np.isclose(results.current_value, 1.0963345074906863)


def test_curr_scores():
    curr = pd.DataFrame(
        {
            "user_id": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3"],
            "item_id": ["0a", "1a", "5a", "6a", "0a", "1a", "5a", "6a", "0a", "4a", "6a", "10a"],
            "item_f1": [1, 1, 1, -0.1, 1, 1, 1, -0.1, 1, 1, -0.1, -1],
            "item_f2": [0, 0.1, 1, 0.9, 0, 0.1, 1, 0.9, 0, 0.9, 0.9, -1],
            "target": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "prediction": [10, 9, 8, 7, 10, 9, 8, 7, 10, 9, 8, 7],
        }
    )
    metric = DiversityMetric(k=4, item_features=["item_f1", "item_f2"])
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.SCORE)
    report.run(reference_data=None, current_data=curr, column_mapping=column_mapping)

    results = metric.get_result()
    assert np.isclose(results.current_value, 1.0963345074906863)
