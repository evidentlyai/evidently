from typing import List

import pandas as pd
import pytest

from evidently.legacy.features.words_feature import ExcludesWords
from evidently.legacy.features.words_feature import IncludesWords
from evidently.legacy.features.words_feature import WordMatch
from evidently.legacy.features.words_feature import WordNoMatch
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

input_data = [
    "Who are you and where are my apples and grapes?",
    "Apple is red",
    "Grape is blue",
]


@pytest.mark.parametrize(
    ["words", "mode", "lemmatize", "expected"],
    [
        (["apple", "grape"], "any", True, [True, True, True]),
        (["apple", "grape"], "all", True, [True, False, False]),
        (["apple", "grape"], "any", False, [False, True, True]),
        (["apple", "grape"], "all", False, [False, False, False]),
    ],
)
def test_includes_words(words: List[str], mode: str, lemmatize: bool, expected: List[bool]):
    feature_generator = IncludesWords("column_1", words_list=words, mode=mode, lemmatize=lemmatize)
    data = pd.DataFrame(dict(column_1=input_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict([(feature_generator._feature_column_name(), expected)])))


@pytest.mark.parametrize(
    ["words", "mode", "lemmatize", "expected"],
    [
        (["apple", "grape"], "any", True, [False, True, True]),
        (["apple", "grape"], "all", True, [False, False, False]),
        (["apple", "grape"], "any", False, [True, True, True]),
        (["apple", "grape"], "all", False, [True, False, False]),
    ],
)
def test_excludes_words(words: List[str], mode: str, lemmatize: bool, expected: List[bool]):
    feature_generator = ExcludesWords("column_1", words_list=words, mode=mode, lemmatize=lemmatize)
    data = pd.DataFrame(dict(column_1=input_data))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict([(feature_generator._feature_column_name(), expected)])))


@pytest.mark.parametrize(
    ["mode", "lemmatize", "expected"],
    [
        ("any", False, [True, True, False, False, False, True]),
        ("all", False, [False, True, False, False, False, True]),
        ("any", True, [False, False, True, True, False, True]),
        ("all", True, [False, False, True, False, False, True]),
    ],
)
def test_word_match(mode: str, lemmatize: bool, expected: List[bool]):
    data = {
        "generated": [
            "I love eating apples and grapes.",
            "I eat apples, grapes, and oranges",
            "Grapes, oranges, apples.",
            "Oranges are more sour than grapes.",
            "This test doesn't have the words.",
            "You are allowed to cancel at any time, and we guarantee that you will receive a refund.",
        ],
        "expected": [
            ["apples", "grapes", "oranges"],
            ["grapes", "apples", "oranges"],
            ["apple", "orange", "grape"],
            ["orange", "sweet", "grape"],
            ["none", "of", "these"],
            ["guarantee", "allowed", "refund"],
        ],
    }
    df = pd.DataFrame(data)
    df["expected"] = df["expected"].apply(tuple)
    feature_generator = WordMatch(columns=["generated", "expected"], mode=mode, lemmatize=lemmatize)
    result = feature_generator.generate_feature(
        data=df,
        data_definition=create_data_definition(None, df, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict([(feature_generator._feature_name(), expected)])))
    column_obj = feature_generator._as_column()
    assert column_obj.display_name == f"Text contains {mode} defined words"


@pytest.mark.parametrize(
    ["mode", "lemmatize", "expected"],
    [
        ("any", False, [True, False, True, True, True, False]),
        ("all", False, [False, False, True, True, True, False]),
        ("any", True, [True, True, False, True, True, False]),
        ("all", True, [True, True, False, False, True, False]),
    ],
)
def test_word_no_match(mode: str, lemmatize: bool, expected: List[bool]):
    data = {
        "generated": [
            "I love eating apples and grapes.",
            "I eat apples, grapes, and oranges",
            "Grapes, oranges, apples.",
            "Oranges are more sour than grapes.",
            "This test doesn't have the words.",
            "You are allowed to cancel at any time, and we guarantee that you will receive a refund.",
        ],
        "forbidden": [
            ["apples", "grapes", "oranges"],
            ["grapes", "apples", "oranges"],
            ["apple", "orange", "grape"],
            ["orange", "sweet", "grape"],
            ["none", "of", "these"],
            ["guarantee", "allowed", "refund"],
        ],
    }
    df = pd.DataFrame(data)
    df["forbidden"] = df["forbidden"].apply(tuple)
    feature_generator = WordNoMatch(columns=["generated", "forbidden"], mode=mode, lemmatize=lemmatize)
    result = feature_generator.generate_feature(
        data=df,
        data_definition=create_data_definition(None, df, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict([(feature_generator._feature_name(), expected)])))
    column_obj = feature_generator._as_column()
    assert column_obj.display_name == f"Text does not contain {mode} defined words"
