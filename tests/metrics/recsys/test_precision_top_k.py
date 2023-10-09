import numpy as np
import pandas as pd

from evidently.metrics import PrecisionTopKMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


def test_precision_value():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recomendations_type="rank")
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[1] == 0.5
    assert results.current[2] == 0.25
    assert np.isclose(results.current[3], 0.333333)


def test_precision_value_judged_only():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recomendations_type="rank")
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[1], 0.333333)
    assert np.isclose(results.current[2], 0.166666)
    assert np.isclose(results.current[3], 0.222222)


def test_precision_value_judged_only_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = PrecisionTopKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[1], 0.333333)
    assert np.isclose(results.current[2], 0.166666)
    assert np.isclose(results.current[3], 0.222222)
