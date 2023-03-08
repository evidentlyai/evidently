import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.metrics import ClassificationConfusionMatrix
from evidently.report import Report


@pytest.mark.parametrize(
    "current, expected_labels, expected_matrix",
    [
        (
            pd.DataFrame(
                data=dict(
                    target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                    prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                )
            ),
            ["a", "b", "c"],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ),
        (
            pd.DataFrame(
                data=dict(
                    target=["a", "a", "a", "a", "a", "b", "b", "b", "b"],
                    prediction=["a", "b", "b", "a", "b", "a", "a", "b", "b"],
                )
            ),
            ["a", "b"],
            [[2, 3], [2, 2]],
        ),
        (
            pd.DataFrame(
                data=dict(
                    target=["c", "c", "c", "b", "b", "b", "a", "a", "a"],
                    prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
                )
            ),
            ["a", "b", "c"],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ),
    ],
)
def test_confusion_matrix(current, expected_labels, expected_matrix):
    metric = ClassificationConfusionMatrix(None, None)
    report = Report(metrics=[metric])
    report.run(
        current_data=current, reference_data=None, column_mapping=ColumnMapping()
    )
    results = metric.get_result()

    assert results.reference_matrix is None

    assert results.current_matrix.labels == expected_labels
    assert results.current_matrix.values == expected_matrix
