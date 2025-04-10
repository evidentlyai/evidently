import numpy as np
import pandas as pd

from evidently.legacy.metrics import FBetaTopKMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_fbeta_values():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = FBetaTopKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[0] == 0.5
    assert np.isclose(results.current[1], 0.33333333333333)
    assert np.isclose(results.current[2], 0.49999962499990)


def test_fbeta_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = FBetaTopKMetric(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[0] == 0.5
    assert np.isclose(results.current[1], 0.33333333333333)
    assert np.isclose(results.current[2], 0.49999962499990)


def test_fbeta_scores_include_no_feedback():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = FBetaTopKMetric(k=3, no_feedback_users=True)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert np.isclose(results.current[0], 0.33333333333)
    assert np.isclose(results.current[1], 0.22222222222)
    assert np.isclose(results.current[2], 0.33333333333)
