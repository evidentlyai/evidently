import pandas as pd
import pytest

from evidently.core.datasets import ColumnTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import TestSummary
from evidently.core.datasets import TestSummaryInfo
from evidently.tests import eq


def _dataset_with_row_tests() -> Dataset:
    dataset = Dataset.from_pandas(pd.DataFrame({"a": [1, 2, 3]}))
    dataset.add_descriptor(ColumnTest("a", eq(1)))
    return dataset


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({"success_all": False}, id="only-default-off"),
        pytest.param(
            {"success_all": False, "success_any": False, "success_count": False, "success_rate": False, "score": False},
            id="all-off",
        ),
    ],
)
def test_test_summary_without_columns_fails(kwargs: dict):
    """A TestSummary that computes nothing must not be accepted silently.

    Every flag turned off leaves no summary column behind, so the descriptor registers a
    `TestSummaryInfo` without any column and the report renders an empty row test summary panel.
    """
    dataset = _dataset_with_row_tests()

    with pytest.raises(ValueError, match="No summary columns specified"):
        dataset.add_descriptor(TestSummary(alias="res", **kwargs))

    assert "res" not in dataset.as_dataframe().columns
    assert not any(isinstance(info, TestSummaryInfo) for info in dataset.data_definition.special_columns)
