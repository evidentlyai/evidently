import pandas as pd
import pytest

from evidently import Report
from evidently.core.datasets import Dataset
from evidently.descriptors import ExcludesWords
from evidently.descriptors import IncludesWords
from evidently.descriptors import TextMatch
from evidently.descriptors import WordMatch
from evidently.metrics import CategoryCount


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "description": [
                "This is urgent and important message",
                "This is just a test message",
                "URGENT: Please respond immediately",
                "Normal message without keywords",
                "Contains both urgent and important words",
                "Spam test message for filtering",
                "Empty message",
                "Message with numbers 123 and symbols @#$",
            ],
            "keywords": [
                ["urgent", "important"],
                ["test"],
                ["urgent"],
                [],
                ["urgent", "important"],
                ["spam", "test"],
                [],
                ["numbers"],
            ],
            "single_keyword": [
                "urgent",
                "test",
                "urgent",
                "",
                "urgent",
                "spam",
                "",
                "numbers",
            ],
        }
    )


@pytest.fixture
def sample_dataset(sample_data):
    return Dataset.from_pandas(sample_data)


def test_contains_any_mode(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["urgent", "important"],
        match_type="contains",
        match_mode="any",
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_contains_all_mode(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["urgent", "important"],
        match_type="contains",
        match_mode="all",
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, False, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_not_contains_any_mode(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["spam", "test"],
        match_type="not_contains",
        match_mode="any",
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, True, True, True, True, False, True, True]
    assert result.data.tolist() == expected


def test_not_contains_all_mode(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["spam", "test"],
        match_type="not_contains",
        match_mode="all",
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, True, True, False, True, True]
    assert result.data.tolist() == expected


def test_exact_match(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=["urgent", "test"], match_type="exact", case_sensitive=False
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [False, False, False, False, False, False, False, False]
    assert result.data.tolist() == expected


def test_regex_match(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=[r"\b(urgent|important)\b"], match_type="regex", case_sensitive=False
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_case_sensitive_true(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=["URGENT"], match_type="contains", case_sensitive=True
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [False, False, True, False, False, False, False, False]
    assert result.data.tolist() == expected


def test_case_sensitive_false(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=["URGENT"], match_type="contains", case_sensitive=False
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_column_to_column_contains(sample_dataset):
    descriptor = TextMatch(column_name="description", match_items="keywords", match_type="contains", match_mode="any")
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, True, False, False, True, True, False, True]
    assert result.data.tolist() == expected


def test_column_to_column_not_contains(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items="keywords", match_type="not_contains", match_mode="any"
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [False, False, True, False, False, True, False, False]
    assert result.data.tolist() == expected


def test_word_boundaries(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["urgent"],
        match_type="contains",
        word_boundaries=True,
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_lemmatization(sample_dataset):
    descriptor = TextMatch(
        column_name="description",
        match_items=["filtering"],
        match_type="contains",
        lemmatize=True,
        word_boundaries=True,
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [False, False, False, False, False, True, False, False]
    assert result.data.tolist() == expected


def test_empty_items_list(sample_dataset):
    descriptor = TextMatch(column_name="description", match_items=[], match_type="contains", match_mode="any")
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [False] * len(sample_dataset.as_dataframe())
    assert result.data.tolist() == expected


def test_single_item_list(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=["urgent"], match_type="contains", case_sensitive=False
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    expected = [True, False, True, False, True, False, False, False]
    assert result.data.tolist() == expected


def test_none_values(sample_dataset):
    df = sample_dataset.as_dataframe()
    df.loc[len(df)] = {"description": None, "keywords": [], "single_keyword": ""}
    dataset_with_none = Dataset.from_pandas(df)

    descriptor = TextMatch(column_name="description", match_items=["urgent"], match_type="contains")
    dataset_with_none.add_descriptor(descriptor)
    result = dataset_with_none.column(descriptor.alias)

    assert not result.data.iloc[-1]


def test_missing_column(sample_dataset):
    descriptor = TextMatch(column_name="nonexistent_column", match_items=["urgent"], match_type="contains")

    with pytest.raises(ValueError, match="Column 'nonexistent_column' is not found in dataset.*"):
        sample_dataset.add_descriptor(descriptor)


def test_missing_match_column(sample_dataset):
    descriptor = TextMatch(column_name="description", match_items="nonexistent_column", match_type="contains")

    with pytest.raises(ValueError, match="Column 'nonexistent_column' is not found in dataset.*"):
        sample_dataset.add_descriptor(descriptor)


def test_regex_multiple_patterns_error(sample_dataset):
    descriptor = TextMatch(
        column_name="description", match_items=[r"\b(urgent|important)\b", r"\btest\b"], match_type="regex"
    )

    with pytest.raises(ValueError, match="Regex matching requires exactly one pattern.*"):
        sample_dataset.add_descriptor(descriptor)


def test_invalid_match_type():
    with pytest.raises(ValueError, match=".*match_type\n  unexpected value.*"):
        TextMatch(
            column_name="description",
            match_items=["urgent"],
            match_type="invalid",  # type: ignore
        )


@pytest.mark.parametrize("match_type", ["contains", "not_contains", "exact", "regex"])
@pytest.mark.parametrize("match_mode", ["any", "all"])
@pytest.mark.parametrize("case_sensitive", [True, False])
def test_parameter_combinations(sample_dataset, match_type, match_mode, case_sensitive):
    if match_type == "exact" and match_mode == "all":
        pytest.skip("Exact match doesn't use match_mode")
    if match_type == "regex":
        pytest.skip("Regex match doesn't use match_mode")

    descriptor = TextMatch(
        column_name="description",
        match_items=["urgent", "important"],
        match_type=match_type,
        match_mode=match_mode,
        case_sensitive=case_sensitive,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    assert len(result.data) == len(sample_dataset.as_dataframe())
    assert all(isinstance(x, bool) for x in result.data)


@pytest.mark.parametrize("lemmatize", [True, False])
@pytest.mark.parametrize("word_boundaries", [True, False])
def test_processing_combinations(sample_dataset, lemmatize, word_boundaries):
    descriptor = TextMatch(
        column_name="description",
        match_items=["urgent"],
        match_type="contains",
        lemmatize=lemmatize,
        word_boundaries=word_boundaries,
        case_sensitive=False,
    )
    sample_dataset.add_descriptor(descriptor)
    result = sample_dataset.column(descriptor.alias)

    assert len(result.data) == len(sample_dataset.as_dataframe())
    assert all(isinstance(x, bool) for x in result.data)


def test_alias_generation_list_items():
    descriptor = TextMatch(
        column_name="description", match_items=["urgent", "important"], match_type="contains", match_mode="any"
    )
    assert descriptor.alias is not None
    assert "description" in descriptor.alias
    assert "contains" in descriptor.alias


def test_alias_generation_column_items():
    descriptor = TextMatch(column_name="description", match_items="keywords", match_type="contains", match_mode="all")
    assert descriptor.alias is not None
    assert "description" in descriptor.alias
    assert "keywords" in descriptor.alias


def test_custom_alias():
    custom_alias = "custom_text_match"
    descriptor = TextMatch(column_name="description", match_items=["urgent"], match_type="contains", alias=custom_alias)
    assert descriptor.alias == custom_alias


def test_list_items_input_columns():
    descriptor = TextMatch(column_name="description", match_items=["urgent", "important"], match_type="contains")
    input_columns = descriptor.list_input_columns()
    assert input_columns == ["description"]


def test_column_items_input_columns():
    descriptor = TextMatch(column_name="description", match_items="keywords", match_type="contains")
    input_columns = descriptor.list_input_columns()
    assert set(input_columns) == {"description", "keywords"}


@pytest.mark.parametrize("route", ["fixed", "substring", "column", "includes_words", "word_match", "excludes_words"])
def test_whole_word_public_descriptors(route):
    texts = ["cat", "A cat.", "concatenate", "bobcat", "scatter", "CAT", "dog", "", None, float("nan")]
    dataset = Dataset.from_pandas(pd.DataFrame({"response": texts, "terms": ["cat"] * len(texts)}))
    expected = [True, True, False, False, False, True, False, False, False, False]
    if route == "fixed":
        descriptor = TextMatch("response", ["cat"], word_boundaries=True, case_sensitive=False, alias="hit")
    elif route == "substring":
        descriptor = TextMatch("response", ["cat"], word_boundaries=False, case_sensitive=False, alias="hit")
        expected = [True, True, True, True, True, True, False, False, False, False]
    elif route == "column":
        descriptor = TextMatch("response", "terms", word_boundaries=True, case_sensitive=False, alias="hit")
    elif route == "includes_words":
        descriptor = IncludesWords("response", ["cat"], lemmatize=False, alias="hit")
    elif route == "word_match":
        descriptor = WordMatch(["response", "terms"], lemmatize=False, alias="hit")
    else:
        descriptor = ExcludesWords("response", ["cat"], lemmatize=False, alias="hit")
        expected = [False, False, True, True, True, False, True, True, True, True]
    dataset.add_descriptor(descriptor)
    assert dataset.column("hit").data.tolist() == expected


@pytest.mark.parametrize(
    "text,item,expected",
    [
        ("a red cat.", "red cat", True),
        ("tired cat", "red cat", False),
        ("red catfish", "red cat", False),
        ("cat-dog", "cat dog", True),
        ("cat dog", "cat  dog", False),
        ("cat-dog", "cat", True),
        ("cat,dog", "cat", True),
        ("_cat", "cat", False),
        ("cat_2", "cat", False),
        ("cat2", "cat", False),
        ("Le café!", "café", True),
        ("caféteria", "café", False),
        ("猫", "猫", True),
        ("猫咪", "猫", False),
        ("cat", "c.t", False),
        ("cat", "cat[", False),
        ("dog", "cat|dog", False),
        ("cat.", "cat.", False),
        ("a cat dog", " cat ", True),
        ("cat dog", " ", True),
    ],
)
def test_whole_word_literal_terms(text, item, expected):
    dataset = Dataset.from_pandas(pd.DataFrame({"response": [text]}))
    dataset.add_descriptor(TextMatch("response", [item], word_boundaries=True, case_sensitive=False, alias="hit"))
    assert dataset.column("hit").data.tolist() == [expected]


@pytest.mark.parametrize("case_sensitive,expected", [(True, False), (False, True)])
def test_whole_word_case_sensitive(case_sensitive, expected):
    dataset = Dataset.from_pandas(pd.DataFrame({"response": ["CAT"]}))
    dataset.add_descriptor(
        TextMatch("response", ["cat"], word_boundaries=True, case_sensitive=case_sensitive, alias="hit")
    )
    assert dataset.column("hit").data.tolist() == [expected]


@pytest.mark.parametrize(
    "match_type,match_mode,expected",
    [
        ("contains", "any", [True, True, True, False]),
        ("contains", "all", [True, False, False, False]),
        ("not_contains", "any", [False, True, True, True]),
        ("not_contains", "all", [False, False, False, True]),
    ],
)
def test_whole_word_any_all_modes(match_type, match_mode, expected):
    dataset = Dataset.from_pandas(
        pd.DataFrame({"response": ["cat dog", "bobcat dog", "cat dogfish", "bobcat dogfish"]})
    )
    dataset.add_descriptor(
        TextMatch(
            "response", ["cat", "dog"], match_type=match_type, match_mode=match_mode, word_boundaries=True, alias="hit"
        )
    )
    assert dataset.column("hit").data.tolist() == expected


@pytest.mark.parametrize(
    "items,match_type,match_mode,expected",
    [
        ([], "contains", "any", False),
        ([], "contains", "all", True),
        ([], "not_contains", "any", False),
        ([], "not_contains", "all", True),
        ([""], "contains", "any", True),
        ([""], "contains", "all", True),
        ([""], "not_contains", "any", False),
        ([""], "not_contains", "all", False),
    ],
)
def test_whole_word_empty_items(items, match_type, match_mode, expected):
    dataset = Dataset.from_pandas(pd.DataFrame({"response": ["cat", "", None]}))
    dataset.add_descriptor(
        TextMatch("response", items, match_type=match_type, match_mode=match_mode, word_boundaries=True, alias="hit")
    )
    assert dataset.column("hit").data.tolist() == [expected] * 3


@pytest.mark.parametrize(
    "match_type,item,text,expected",
    [
        ("exact", "cat dog", "cat-dog", True),
        ("exact", "cat-dog", "cat-dog", False),
        ("regex", r"\bcat\b", "bobcat", False),
        ("regex", "cat", "bobcat", True),
        ("regex", "cat dog", "cat-dog", True),
        ("regex", r"cat\-dog", "cat-dog", False),
    ],
)
def test_whole_word_exact_regex_unchanged(match_type, item, text, expected):
    dataset = Dataset.from_pandas(pd.DataFrame({"response": [text]}))
    dataset.add_descriptor(TextMatch("response", [item], match_type=match_type, word_boundaries=True, alias="hit"))
    assert dataset.column("hit").data.tolist() == [expected]


def test_whole_word_report_count():
    dataset = Dataset.from_pandas(pd.DataFrame({"response": ["cat", "bobcat", "dog"]}))
    dataset.add_descriptor(TextMatch("response", ["cat"], word_boundaries=True, alias="hit"))
    result = Report([CategoryCount(column="hit", categories=[True])]).run(dataset).dict()["metrics"][0]["value"]
    assert result["count"] == 1
    assert result["share"] == pytest.approx(1 / 3)
