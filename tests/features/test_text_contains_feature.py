from typing import List

import pandas as pd
import pytest

from evidently.legacy.features.text_contains_feature import Contains
from evidently.legacy.features.text_contains_feature import DoesNotContain
from evidently.legacy.features.text_contains_feature import ItemMatch
from evidently.legacy.features.text_contains_feature import ItemNoMatch
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

test_data = [
    "a b c d e f g h",
    "b c d e f g h",
    "h",
    "A",
    "a B c D",
]


@pytest.mark.parametrize(
    ("items", "case", "mode", "expected"),
    [
        (["a"], True, "any", [True, False, False, False, True]),
        (["b"], True, "any", [True, True, False, False, False]),
        (["a"], False, "any", [True, False, False, True, True]),
        (["b"], False, "any", [True, True, False, False, True]),
        (["a", "b"], True, "any", [True, True, False, False, True]),
        (["a", "b"], True, "all", [True, False, False, False, False]),
        (["a", "b"], False, "any", [True, True, False, True, True]),
        (["a", "b"], False, "all", [True, False, False, False, True]),
    ],
)
def test_text_contains_feature(items: List[str], case: bool, mode: str, expected: List[bool]):
    feature_generator = Contains("column_1", items, case_sensitive=case, mode=mode)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)


@pytest.mark.parametrize(
    ("items", "case", "mode", "expected"),
    [
        (["a", "b"], True, "any", [False, False, True, True, False]),
        (["a", "b"], True, "all", [False, True, True, True, True]),
        (["a", "b"], False, "any", [False, False, True, False, False]),
        (["a", "b"], False, "all", [False, True, True, True, False]),
    ],
)
def test_text_not_contains_feature(items: List[str], case: bool, mode: str, expected: List[bool]):
    feature_generator = DoesNotContain("column_1", items, case_sensitive=case, mode=mode)
    data = pd.DataFrame(dict(column_1=test_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)


@pytest.mark.parametrize(
    ("case", "mode", "expected"),
    [
        (True, "any", [False, True, False, True, False]),
        (True, "all", [False, True, False, False, False]),
        (False, "any", [True, True, True, True, False]),
        (False, "all", [False, True, True, False, False]),
    ],
)
def test_item_match(case: bool, mode: str, expected: List[bool]):
    data = {
        "generated": [
            "You should consider purchasing Nike or Adidas shoes.",
            "I eat apples, grapes, and oranges",
            "grapes, oranges, apples.",
            "Oranges are more sour than grapes.",
            "This test doesn't have the words.",
        ],
        "expected": [
            ["nike", "adidas", "puma"],
            ["grapes", "apples", "oranges"],
            ["Apples", "Oranges", "Grapes"],
            ["orange", "sweet", "grape"],
            ["none", "of", "these"],
        ],
    }
    df = pd.DataFrame(data)
    df["expected"] = df["expected"].apply(tuple)
    feature_generator = ItemMatch(columns=["generated", "expected"], case_sensitive=case, mode=mode)
    result = feature_generator.generate_feature(
        data=df,
        data_definition=create_data_definition(None, df, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    column_name_obj = feature_generator._as_column()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)
    assert column_name_obj.display_name == f"Text contains {mode} of defined items"


@pytest.mark.parametrize(
    ("case", "mode", "expected"),
    [
        (True, "any", [True, False, True, False, True]),
        (True, "all", [True, False, True, True, True]),
        (False, "any", [False, False, False, False, True]),
        (False, "all", [True, False, False, True, True]),
    ],
)
def test_item_no_match(case: bool, mode: str, expected: List[bool]):
    data = {
        "generated": [
            "You should consider purchasing Nike or Adidas shoes.",
            "I eat apples, grapes, and oranges",
            "grapes, oranges, apples.",
            "Oranges are more sour than grapes.",
            "This test doesn't have the words.",
        ],
        "forbidden": [
            ["nike", "adidas", "puma"],
            ["grapes", "apples", "oranges"],
            ["Apples", "Oranges", "Grapes"],
            ["orange", "sweet", "grape"],
            ["none", "of", "these"],
        ],
    }
    feature_generator = ItemNoMatch(columns=["generated", "forbidden"], case_sensitive=case, mode=mode)
    df = pd.DataFrame(data)
    df["forbidden"] = df["forbidden"].apply(tuple)
    result = feature_generator.generate_feature(
        data=df,
        data_definition=create_data_definition(None, df, ColumnMapping()),
    )
    column_expected = feature_generator._feature_column_name()
    column_name_obj = feature_generator._as_column()
    expected_df = pd.DataFrame({column_expected: expected})
    assert result.equals(expected_df)
    assert column_name_obj.display_name == f"Text does not contain {mode} of defined items"
