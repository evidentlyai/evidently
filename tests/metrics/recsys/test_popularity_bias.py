import pandas as pd
import pytest

from evidently.legacy.metrics import PopularityBias
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.report import Report


@pytest.mark.parametrize("k, expected_coverage", ((1, 1 / 3.0), (2, 2 / 3.0), (3, 1.0)))
def test_coverage(k, expected_coverage):
    curr = pd.DataFrame(
        {
            "user_id": [1, 1, 1, 2, 2, 2, 3, 3, 3],
            "item_id": [1, 2, 3, 1, 2, 3, 1, 2, 3],
            "prediction": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        }
    )

    train = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 3],
            "item_id": [1, 2, 1, 3],
        }
    )

    metric = PopularityBias(k=k)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": train},
    )

    results = metric.get_result()
    assert results.current_coverage == expected_coverage


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
    metric = PopularityBias(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.RANK)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": train},
    )

    results = metric.get_result()
    assert results.current_apr == 1.5
    assert results.current_coverage == 1.0
    assert results.current_gini == 0.2


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
    metric = PopularityBias(k=3)
    report = Report(metrics=[metric])
    column_mapping = ColumnMapping(recommendations_type=RecomType.SCORE)
    report.run(
        reference_data=None,
        current_data=curr,
        column_mapping=column_mapping,
        additional_data={"current_train_data": train},
    )

    results = metric.get_result()
    assert results.current_apr == 1.5
    assert results.current_coverage == 1.0
    assert results.current_gini == 0.2
