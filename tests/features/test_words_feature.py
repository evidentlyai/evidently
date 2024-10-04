from typing import List

import pandas as pd
import pytest

from evidently.features.words_feature import ExcludesWords
from evidently.features.words_feature import IncludesWords
from evidently.features.words_feature import WordMatchFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition

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


input_data = [
    "Who are you and where are my apples and grapes?",
    "Apple is red",
    "Grape is blue",
]


@pytest.mark.parametrize(
    ["mode", "lemmatize", "expected"],
    [
        ("any", False, [True, True, False, False]),
        ("all", False, [False, True, False, False]),
        ("all", True, [False, True, True, False]),
        ("all", False, [False, True, False, False]),
    ],
)
def test_word_match(mode: str, lemmatize: bool, expected: List[bool]):
    data = {
        "generated": [
            "I love eating apples and grapes.",
            "I love apples, grapes, and oranges",
            "Grapes, oranges, apples.",
            "Oranges are more sour than grapes.",
        ],
        "expected": [
            ["apples", "grapes", "oranges"],
            ["grapes", "apples", "oranges"],
            ["apple", "orange", "grape"],
            ["orange", "sweet", "grape"],
        ],
    }
    df = pd.DataFrame(data)
    df["expected"] = df["expected"].apply(tuple)
    feature_generator = WordMatchFeature(columns=["generated", "expected"], mode=mode, lemmatize=lemmatize)
    result = feature_generator.generate_feature(
        data=df,
        data_definition=create_data_definition(None, df, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict([(feature_generator._feature_name(), expected)])))
