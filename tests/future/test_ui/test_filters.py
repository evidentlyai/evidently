import numpy as np
import pandas as pd
import pytest

from evidently.ui.service.datasets.filters import ContainsStrFilter
from evidently.ui.service.datasets.filters import EndsWithFilter
from evidently.ui.service.datasets.filters import EqualFilter
from evidently.ui.service.datasets.filters import GTEFilter
from evidently.ui.service.datasets.filters import GTFilter
from evidently.ui.service.datasets.filters import LTEFilter
from evidently.ui.service.datasets.filters import LTFilter
from evidently.ui.service.datasets.filters import NotEqualFilter
from evidently.ui.service.datasets.filters import StartsWithFilter
from evidently.ui.service.datasets.filters import filter_df


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "score": [85.5, 90.0, 75.5, 95.0, 88.5],
            "city": ["New York", "London", "Paris", "Tokyo", "Berlin"],
        }
    )


def test_contains_str_filter(sample_dataframe):
    """Test ContainsStrFilter."""
    filter_obj = ContainsStrFilter(column="name", value="li")
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 2  # Alice, Charlie
    filtered = sample_dataframe[condition]
    assert len(filtered) == 2
    assert "Alice" in filtered["name"].values
    assert "Charlie" in filtered["name"].values


def test_starts_with_filter(sample_dataframe):
    """Test StartsWithFilter."""
    filter_obj = StartsWithFilter(column="name", value="C")
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 1  # Charlie
    filtered = sample_dataframe[condition]
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "Charlie"


def test_ends_with_filter(sample_dataframe):
    """Test EndsWithFilter."""
    filter_obj = EndsWithFilter(column="name", value="e")
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 3  # Alice, Charlie, Eve
    filtered = sample_dataframe[condition]
    assert len(filtered) == 3
    assert "Alice" in filtered["name"].values
    assert "Charlie" in filtered["name"].values
    assert "Eve" in filtered["name"].values


def test_equal_filter(sample_dataframe):
    """Test EqualFilter."""
    filter_obj = EqualFilter(column="age", value=30)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 1  # Bob
    filtered = sample_dataframe[condition]
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "Bob"
    assert filtered.iloc[0]["age"] == 30


def test_not_equal_filter(sample_dataframe):
    """Test NotEqualFilter."""
    filter_obj = NotEqualFilter(column="age", value=30)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 4  # Everyone except Bob
    filtered = sample_dataframe[condition]
    assert len(filtered) == 4
    assert "Bob" not in filtered["name"].values


def test_gt_filter(sample_dataframe):
    """Test GTFilter."""
    filter_obj = GTFilter(column="age", value=35)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 2  # David (40), Eve (45)
    filtered = sample_dataframe[condition]
    assert len(filtered) == 2
    assert all(filtered["age"] > 35)


def test_gte_filter(sample_dataframe):
    """Test GTEFilter."""
    filter_obj = GTEFilter(column="age", value=35)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 3  # Charlie (35), David (40), Eve (45)
    filtered = sample_dataframe[condition]
    assert len(filtered) == 3
    assert all(filtered["age"] >= 35)


def test_lt_filter(sample_dataframe):
    """Test LTFilter."""
    filter_obj = LTFilter(column="age", value=35)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 2  # Alice (25), Bob (30)
    filtered = sample_dataframe[condition]
    assert len(filtered) == 2
    assert all(filtered["age"] < 35)


def test_lte_filter(sample_dataframe):
    """Test LTEFilter."""
    filter_obj = LTEFilter(column="age", value=35)
    condition = filter_obj.condition(sample_dataframe)
    assert condition.sum() == 3  # Alice (25), Bob (30), Charlie (35)
    filtered = sample_dataframe[condition]
    assert len(filtered) == 3
    assert all(filtered["age"] <= 35)


def test_filter_df_single_filter(sample_dataframe):
    """Test filter_df with a single filter."""
    filters = [EqualFilter(column="age", value=30)]
    filtered = filter_df(sample_dataframe, filters)
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "Bob"


def test_filter_df_multiple_filters(sample_dataframe):
    """Test filter_df with multiple filters (AND logic)."""
    filters = [
        GTEFilter(column="age", value=30),
        LTFilter(column="age", value=40),
    ]
    filtered = filter_df(sample_dataframe, filters)
    assert len(filtered) == 2  # Bob (30), Charlie (35)
    assert "Bob" in filtered["name"].values
    assert "Charlie" in filtered["name"].values
    assert all(30 <= age < 40 for age in filtered["age"])


def test_filter_df_no_filters(sample_dataframe):
    """Test filter_df with no filters."""
    filtered = filter_df(sample_dataframe, None)
    assert len(filtered) == len(sample_dataframe)
    pd.testing.assert_frame_equal(filtered, sample_dataframe)


def test_filter_df_empty_list(sample_dataframe):
    """Test filter_df with empty filter list."""
    filtered = filter_df(sample_dataframe, [])
    assert len(filtered) == len(sample_dataframe)
    pd.testing.assert_frame_equal(filtered, sample_dataframe)


def test_filter_df_combined_string_and_number(sample_dataframe):
    """Test filter_df with both string and number filters."""
    filters = [
        ContainsStrFilter(column="name", value="a"),
        GTFilter(column="score", value=80.0),
    ]
    filtered = filter_df(sample_dataframe, filters)
    # Names with 'a' (case-insensitive): Alice, Charlie, David
    # Scores > 80: Alice (85.5), Bob (90.0), David (95.0), Eve (88.5)
    # Combined: Alice (has 'a' and score 85.5 > 80), David (has 'a' and score 95.0 > 80)
    # Charlie has 'a' but score 75.5 <= 80, so filtered out
    # Note: ContainsStrFilter is case-sensitive, so "Alice" doesn't match "a"
    # Only "David" matches (contains lowercase 'a' in "David")
    assert len(filtered) == 1
    assert "David" in filtered["name"].values


def test_filter_df_with_nan_values():
    """Test filter_df with NaN values."""
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", None, "David"],
            "age": [25, 30, np.nan, 40],
        }
    )
    filter_obj = EqualFilter(column="age", value=30)
    condition = filter_obj.condition(df)
    filtered = df[condition]
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "Bob"


def test_filter_df_missing_column(sample_dataframe):
    """Test filter_df with non-existent column."""
    filter_obj = EqualFilter(column="nonexistent", value=10)
    with pytest.raises(KeyError):
        filter_obj.condition(sample_dataframe)


def test_filter_df_empty_dataframe():
    """Test filter_df with empty dataframe."""
    empty_df = pd.DataFrame({"col1": [], "col2": []})
    filters = [EqualFilter(column="col1", value=1)]
    filtered = filter_df(empty_df, filters)
    assert len(filtered) == 0
