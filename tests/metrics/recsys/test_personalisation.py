import numpy as np
import pandas as pd

from evidently.metrics import PersonalisationMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


def test_curr_rank():
    curr = pd.DataFrame(
        {
            "user_id": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
            "item_id": [1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 2, 5],
            "prediction": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
        }
    )
    metric = PersonalisationMetric(k=4)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type="rank")
    report.run(reference_data=None, current_data=curr, column_mapping=column_mapping)

    results = metric.get_result()
    assert np.isclose(results.current_value, 0.16666666)


def test_curr_scores():
    curr = pd.DataFrame(
        {
            "user_id": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
            "item_id": [1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 2, 5],
            "prediction": [10, 9, 8, 4, 10, 9, 8, 4, 10, 9, 8, 4],
        }
    )
    metric = PersonalisationMetric(k=4)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type="score")
    report.run(reference_data=None, current_data=curr, column_mapping=column_mapping)

    results = metric.get_result()
    assert np.isclose(results.current_value, 0.16666666)
