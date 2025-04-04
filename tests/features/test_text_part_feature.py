from typing import List

import pandas as pd
import pytest

from evidently.legacy.features.text_part_feature import BeginsWith
from evidently.legacy.features.text_part_feature import EndsWith
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

test_data = [
    "abcdefg",
    "aBcdeFg",
    "cdefg",
    "abcde",
    "abfg",
]


@pytest.mark.parametrize(
    ("substr", "case", "expected"),
    [
        ("abc", True, [True, False, False, True, False]),
        ("abc", False, [True, True, False, True, False]),
        ("ABC", False, [True, True, False, True, False]),
    ],
)
def test_text_begins_feature(substr: str, case: bool, expected: List[bool]):
    feature_generator = BeginsWith("column_1", substr, case_sensitive=case)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)


@pytest.mark.parametrize(
    ("substr", "case", "expected"),
    [
        ("efg", True, [True, False, True, False, False]),
        ("efg", False, [True, True, True, False, False]),
    ],
)
def test_text_ends_feature(substr: str, case: bool, expected: List[bool]):
    feature_generator = EndsWith("column_1", substr, case_sensitive=case)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)
