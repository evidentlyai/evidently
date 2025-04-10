import pandas as pd

from evidently.legacy.metrics import MARKMetric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


def test_mar_values():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1, 2, 3, 1, 2, 3, 1, 2, 3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = MARKMetric(k=2)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[0] == 0.5
    assert results.current[1] == 0.5
    assert results.current[2] == 1


def test_mar_scores():
    current = pd.DataFrame(
        data=dict(
            user_id=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=[1.25, 1.0, 0.3, 0.9, 0.8, 0.7, 1.0, 0.5, 0.3],
            target=[1, 0, 0, 0, 0, 0, 0, 0, 1],
        ),
    )

    metric = MARKMetric(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping()
    report.run(reference_data=None, current_data=current, column_mapping=column_mapping)

    results = metric.get_result()
    assert len(results.current) == 3
    assert results.current[0] == 0.5
    assert results.current[1] == 0.5
    assert results.current[2] == 1
