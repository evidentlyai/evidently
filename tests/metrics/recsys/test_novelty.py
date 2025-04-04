import numpy as np
import pandas as pd

from evidently.legacy.metrics import NoveltyMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_curr_rank():
    curr = pd.DataFrame(
        {
            "user_id": [1, 2, 2, 3, 3],
            "item_id": [3, 2, 3, 1, 2],
            "prediction": [1, 1, 2, 1, 2],
        }
    )
    train = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 3],
            "item_id": [1, 2, 1, 1],
        }
    )
    metric = NoveltyMetric(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": train},
    )

    results = metric.get_result()
    assert np.isclose(results.current_value, 1.18872199999)


def test_curr_score():
    curr = pd.DataFrame(
        {
            "user_id": [1, 2, 2, 3, 3],
            "item_id": [3, 2, 3, 1, 2],
            "prediction": [3, 3, 2, 3, 2],
        }
    )
    train = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 3],
            "item_id": [1, 2, 1, 1],
        }
    )
    metric = NoveltyMetric(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.SCORE)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": train},
    )

    results = metric.get_result()
    assert np.isclose(results.current_value, 1.18872199999)
