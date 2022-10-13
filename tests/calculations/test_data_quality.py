import numpy as np
import pandas as pd
import pytest

from evidently.calculations.data_quality import ColumnCorrelations
from evidently.calculations.data_quality import calculate_column_distribution
from evidently.calculations.data_quality import calculate_cramer_v_correlations
from evidently.calculations.data_quality import get_rows_count


@pytest.mark.parametrize(
    "dataset, expected_rows",
    (
        (pd.DataFrame({}), 0),
        (pd.DataFrame({"test": [1, 2, 3]}), 3),
        (pd.DataFrame({"test": [1, 2, None]}), 3),
        (pd.DataFrame({"test": [None, None, None]}), 3),
        (pd.DataFrame({"test": [np.NAN, pd.NA, 2, 0, pd.NaT], "target": [1, 0, 1, 0, 1]}), 5),
    ),
)
def test_get_rows_count(dataset: pd.DataFrame, expected_rows: int) -> None:
    assert get_rows_count(dataset) == expected_rows


@pytest.mark.parametrize(
    "dataset, column_type, expected_distribution",
    (
        (pd.DataFrame({"test": []}), "num", []),
        (pd.DataFrame({"test": [1, 2, 1, 2]}), "num", [(2, 2), (1, 2)]),
        (pd.DataFrame({"test": [1, 2, 1, 2]}), "cat", [(2, 2), (1, 2)]),
    ),
)
def test_calculate_column_distribution(dataset: pd.DataFrame, column_type: str, expected_distribution: list) -> None:
    assert calculate_column_distribution(dataset["test"], column_type=column_type) == expected_distribution


def test_calculate_cramer_v_correlations():
    data = pd.DataFrame(
        {
            "test1": ["a", "b", "c"],
            "test2": ["b", "a", "a"],
            "test3": ["a", "b", "a"],
            "test4": ["a", "b", "c"],
        }
    )
    assert calculate_cramer_v_correlations("test1", data, ["test2", "test3", "test4"]) == ColumnCorrelations(
        column_name="test1", kind="cramer_v", correlations={"test2": 1.0, "test3": 1.0, "test4": 1.0}
    )
