from typing import List

import pandas as pd
import pytest

from evidently.features.text_part_feature import TextPart
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition


test_data = [
    "abcdefg",
    "aBcdeFg",
    "cdefg",
    "abcde",
    "abfg",
]


@pytest.mark.parametrize(("substr", "case", "mode", "expected"), [
    ("abc", True, "prefix", [True, False, False, True, False]),
    ("abc", False, "prefix", [True, True, False, True, False]),
    ("ABC", False, "prefix", [True, True, False, True, False]),
    ("efg", True, "suffix", [True, False, True, False, False]),
    ("efg", False, "suffix", [True, True, True, False, False]),
])
def test_text_contains_feature(substr: str, case: bool, mode: str, expected: List[bool]):
    feature_generator = TextPart("column_1", substr, case_sensitive=case, mode=mode)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=expected)))
