from typing import List

import pandas as pd
import pytest

from evidently.features.text_contains_feature import TextContains
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition


test_data = [
    "a b c d e f g h",
    "b c d e f g h",
    "h",
    "A",
    "a B c D",
]


@pytest.mark.parametrize(("items", "case", "mode", "expected"), [
    (["a"], True, "any", [True, False, False, False, True]),
    (["b"], True, "any", [True, True, False, False, False]),
    (["a"], False, "any", [True, False, False, True, True]),
    (["b"], False, "any", [True, True, False, False, True]),
    (["a", "b"], True, "any", [True, True, False, False, True]),
    (["a", "b"], True, "all", [True, False, False, False, False]),
    (["a", "b"], True, "none", [False, False, True, True, False]),
    (["a", "b"], True, "not_all", [False, True, True, True, True]),
    (["a", "b"], False, "any", [True, True, False, True, True]),
    (["a", "b"], False, "all", [True, False, False, False, True]),
    (["a", "b"], False, "none", [False, False, True, False, False]),
    (["a", "b"], False, "not_all", [False, True, True, True, False]),
])
def test_text_contains_feature(items: List[str], case: bool, mode: str, expected: List[bool]):
    feature_generator = TextContains("column_1", items, case_sensitive=case, mode=mode)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=expected)))
