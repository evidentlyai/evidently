import numpy as np
import pandas as pd
import pytest

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


@pytest.mark.parametrize("beta,expected", [(0.5, 5 / 18), (1.0, 1 / 3), (2.0, 5 / 12)])
def test_fbeta_zero_precision_and_recall(beta, expected):
    metric = FBetaTopKMetric(k=1, beta=beta)
    with np.errstate(divide="raise", invalid="raise"):
        result = metric.fbeta([0.0, 0.25, np.nan], [0.0, 0.5, np.nan])
    np.testing.assert_allclose(result, [0.0, expected, np.nan])


@pytest.mark.parametrize(
    "beta,current_last,reference_second", [(0.5, 5 / 13, 5 / 9), (1.0, 1 / 2, 2 / 3), (2.0, 5 / 7, 5 / 6)]
)
@pytest.mark.parametrize("no_feedback_users", [False, True])
@pytest.mark.parametrize("with_reference", [False, True])
def test_fbeta_no_relevant_items_at_cutoff(beta, current_last, reference_second, no_feedback_users, with_reference):
    current = pd.DataFrame(
        {
            "user_id": ["a", "a", "a", "b", "b", "b"],
            "prediction": [1, 2, 3, 1, 2, 3],
            "target": [0, 0, 1, 0, 0, 0],
        }
    )
    reference = current.assign(target=[0, 1, 0, 0, 0, 0]) if with_reference else None
    metric = FBetaTopKMetric(k=1, beta=beta, no_feedback_users=no_feedback_users)
    Report(metrics=[metric]).run(
        current_data=current,
        reference_data=reference,
        column_mapping=ColumnMapping(recommendations_type=RecomType.RANK),
    )

    result = metric.get_result()
    scale = 0.5 if no_feedback_users else 1.0
    np.testing.assert_allclose(result.current, [0.0, 0.0, current_last * scale])
    assert result.current_value == 0.0
    if with_reference:
        np.testing.assert_allclose(result.reference, [0.0, reference_second * scale, current_last * scale])
        assert result.reference_value == 0.0
    else:
        assert result.reference is None
