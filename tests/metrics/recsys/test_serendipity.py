import numpy as np
import pandas as pd

from evidently.legacy.metrics import SerendipityMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_curr_rank():
    curr = pd.DataFrame(
        {
            "user_id": ["1b", "1b", "1b", "1b", "2b", "2b", "2b", "2b", "3b", "3b", "3b", "3b"],
            "item_id": ["0a", "1a", "5a", "6a", "0a", "1a", "5a", "6a", "0a", "4a", "6a", "10a"],
            "item_f1": [1, 1, 1, -0.1, 1, 1, 1, -0.1, 1, 1, -0.1, -1],
            "item_f2": [0, 0.1, 1, 0.9, 0, 0.1, 1, 0.9, 0, 0.9, 0.9, 0],
            "target": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "prediction": [
                1,
                2,
                3,
                4,
                1,
                2,
                3,
                4,
                1,
                2,
                3,
                4,
            ],
        }
    )
    curr_train = pd.DataFrame(
        {
            "user_id": ["1b", "2b", "3b"],
            "item_id": ["10a", "2a", "5a"],
            "item_f1": [-1, 1, 1],
            "item_f2": [-0, 0.2, 1],
        }
    )
    metric = SerendipityMetric(k=3, item_features=["item_f1", "item_f2"])
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": curr_train},
    )

    results = metric.get_result()
    assert np.isclose(results.current_value, 0.8632630527478137)


def test_curr_scores():
    curr = pd.DataFrame(
        {
            "user_id": ["1b", "1b", "1b", "1b", "2b", "2b", "2b", "2b", "3b", "3b", "3b", "3b"],
            "item_id": ["0a", "1a", "5a", "6a", "0a", "1a", "5a", "6a", "0a", "4a", "6a", "10a"],
            "item_f1": [1, 1, 1, -0.1, 1, 1, 1, -0.1, 1, 1, -0.1, -1],
            "item_f2": [0, 0.1, 1, 0.9, 0, 0.1, 1, 0.9, 0, 0.9, 0.9, 0],
            "target": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "prediction": [100, 20, 3, 1, 100, 20, 3, 1, 100, 20, 3, 1],
        }
    )
    curr_train = pd.DataFrame(
        {
            "user_id": ["1b", "2b", "3b"],
            "item_id": ["10a", "2a", "5a"],
            "item_f1": [-1, 1, 1],
            "item_f2": [-0, 0.2, 1],
        }
    )
    metric = SerendipityMetric(k=3, item_features=["item_f1", "item_f2"])
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.SCORE)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": curr_train},
    )

    results = metric.get_result()
    assert np.isclose(results.current_value, 0.8632630527478137)
