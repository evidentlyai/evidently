import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.data_quality import _cramer_v
from evidently.legacy.calculations.data_quality import calculate_column_distribution
from evidently.legacy.calculations.data_quality import calculate_cramer_v_correlation
from evidently.legacy.calculations.data_quality import get_pairwise_correlation
from evidently.legacy.calculations.data_quality import get_rows_count
from evidently.legacy.metric_results import ColumnCorrelations
from evidently.legacy.metric_results import Distribution


@pytest.mark.parametrize(
    "dataset, expected_rows",
    (
        (pd.DataFrame({}), 0),
        (pd.DataFrame({"test": [1, 2, 3]}), 3),
        (pd.DataFrame({"test": [1, 2, None]}), 3),
        (pd.DataFrame({"test": [None, None, None]}), 3),
        (pd.DataFrame({"test": [np.nan, pd.NA, 2, 0, pd.NaT], "target": [1, 0, 1, 0, 1]}), 5),
    ),
)
def test_get_rows_count(dataset: pd.DataFrame, expected_rows: int) -> None:
    assert get_rows_count(dataset) == expected_rows


@pytest.mark.parametrize(
    "dataset, column_type, expected_distribution",
    (
        (pd.DataFrame({"test": []}), "num", {}),
        (pd.DataFrame({"test": [1, 2, 1, 2]}), "num", {1: 2, 2: 2}),
        (pd.DataFrame({"test": [1, 2, 1, 2]}), "cat", {1: 2, 2: 2}),
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
    assert calculate_cramer_v_correlation("test1", data, ["test2", "test3", "test4"]) == ColumnCorrelations(
        column_name="test1",
        kind="cramer_v",
        values=Distribution(
            x=["test2", "test3", "test4"],
            y=[1.0, 1.0, 1.0],
        ),
    )


def _mutually_exclusive_frame() -> pd.DataFrame:
    # Column "a" is filled exactly when column "b" is null and vice versa,
    # so the pair has no overlapping non-null observations.
    return pd.DataFrame(
        {
            "a": pd.Series(["x", "x", None, None, "y", "y", None, None], dtype=object),
            "b": pd.Series([None, None, "p", "p", None, None, "q", "q"], dtype=object),
        }
    )


def test_cramer_v_mutually_exclusive_columns_returns_nan():
    # Regression test for https://github.com/evidentlyai/evidently/issues/979:
    # pd.crosstab() of two mutually exclusive columns is empty and
    # chi2_contingency() raises `ValueError: No data; 'observed' has size 0.`
    df = _mutually_exclusive_frame()
    assert np.isnan(_cramer_v(df["a"], df["b"]))


def test_cramer_v_normal_case_still_computes():
    df = pd.DataFrame(
        {
            "a": ["x", "x", "y", "y", "x", "y"],
            "b": ["p", "q", "p", "q", "p", "q"],
        }
    )
    value = _cramer_v(df["a"], df["b"])
    assert not np.isnan(value)
    assert 0.0 <= value <= 1.0


def test_calculate_cramer_v_correlation_mutually_exclusive_columns():
    # The column-level helper used by the data-quality metrics must not crash
    # when one of the compared columns is mutually exclusive with the target.
    df = _mutually_exclusive_frame()
    result = calculate_cramer_v_correlation("a", df, ["b"])
    assert result.column_name == "a"
    assert result.kind == "cramer_v"
    assert result.values.x == ["b"]
    assert len(result.values.y) == 1
    assert np.isnan(result.values.y[0])


def test_pairwise_correlation_mutually_exclusive_columns():
    # get_pairwise_correlation() drives DatasetCorrelationsMetric; the matrix
    # must contain NaN for the degenerate pair instead of raising.
    df = _mutually_exclusive_frame()
    matrix = get_pairwise_correlation(df, _cramer_v)
    assert np.isnan(matrix.loc["a", "b"])
    assert np.isnan(matrix.loc["b", "a"])
    assert matrix.loc["a", "a"] == 1.0
