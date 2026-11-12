import numpy as np
import pandas as pd
import pytest

from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import Regression
from evidently.core.report import Report
from evidently.legacy.calculations.regression_performance import _calculate_quality_metrics
from evidently.metrics import MAPE


def _data(index):
    return pd.DataFrame(
        {"target": [0.0, 1.0, 2.0, 0.0, 4.0, 8.0], "prediction": [2.0, 2.0, 1.0, 3.0, 6.0, 8.0]},
        index=index,
    )


@pytest.mark.parametrize(
    "index",
    [
        pd.Index([7, 7, 8, 8, 9, 9]),
        pd.Index(["a", "a", "b", "b", "c", "c"]),
        pd.MultiIndex.from_tuples([("a", 1), ("a", 1), ("a", 2), ("a", 2), ("b", 1), ("b", 1)]),
        pd.RangeIndex(6),
    ],
    ids=["duplicate-integer", "duplicate-string", "duplicate-multiindex", "unique-control"],
)
@pytest.mark.parametrize(
    "handling,relative_errors",
    [("drop", [1.0, 0.5, 0.5, 0.0]), ("replace", [0.25, 1.0, 0.5, 0.25, 0.5, 0.0])],
)
def test_mape_handles_only_the_selected_rows(index, handling, relative_errors):
    data = _data(index)
    original = data.copy(deep=True)

    result = _calculate_quality_metrics(
        data, "prediction", "target", mape_zero_handling=handling, mape_replace_value=0.25
    )

    assert result["mean_abs_perc_error"] == pytest.approx(100 * np.mean(relative_errors))
    assert result["abs_perc_error_std"] == pytest.approx(np.std(relative_errors, ddof=1))
    pd.testing.assert_frame_equal(data, original)


@pytest.mark.parametrize("handling", ["drop", "replace"])
def test_mape_report_is_invariant_to_duplicate_row_labels(handling):
    metric = MAPE(zero_handling=handling, replace_value=0.25, perc_error_plot=False)

    def evaluate(index):
        dataset = Dataset.from_pandas(_data(index), data_definition=DataDefinition(regression=[Regression()]))
        return Report([metric]).run(dataset).dict()["metrics"][0]["value"]

    unique = evaluate(pd.RangeIndex(6))
    duplicated = evaluate(pd.Index([7, 7, 8, 8, 9, 9]))

    assert duplicated == pytest.approx(unique)


def test_mape_without_zero_handling_preserves_duplicate_rows():
    data = _data(pd.Index([7, 7, 8, 8, 9, 9]))
    result = _calculate_quality_metrics(data, "prediction", "target", mape_epsilon=0.5)

    relative_errors = [4.0, 1.0, 0.5, 6.0, 0.5, 0.0]
    assert result["mean_abs_perc_error"] == pytest.approx(100 * np.mean(relative_errors))
    assert result["abs_perc_error_std"] == pytest.approx(np.std(relative_errors, ddof=1))
