import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.datasets import FeatureDescriptor
from evidently.descriptors import Contains
from evidently.descriptors import DoesNotContain
from evidently.descriptors import ExcludesWords
from evidently.descriptors import IncludesWords
from evidently.descriptors import ItemMatch
from evidently.descriptors import ItemNoMatch
from evidently.descriptors import RegExp
from evidently.descriptors import TriggerWordsPresent
from evidently.descriptors import WordMatch
from evidently.descriptors import WordNoMatch
from evidently.descriptors import WordsPresence
from evidently.legacy.features.regexp_feature import RegExp as LegacyRegExp
from evidently.legacy.features.text_contains_feature import Contains as LegacyContains
from evidently.legacy.features.text_contains_feature import DoesNotContain as LegacyDoesNotContain
from evidently.legacy.features.text_contains_feature import ItemMatch as LegacyItemMatch
from evidently.legacy.features.text_contains_feature import ItemNoMatch as LegacyItemNoMatch
from evidently.legacy.features.trigger_words_presence_feature import TriggerWordsPresent as LegacyTriggerWordsPresent
from evidently.legacy.features.words_feature import ExcludesWords as LegacyExcludesWords
from evidently.legacy.features.words_feature import IncludesWords as LegacyIncludesWords
from evidently.legacy.features.words_feature import WordMatch as LegacyWordMatch
from evidently.legacy.features.words_feature import WordNoMatch as LegacyWordNoMatch
from evidently.legacy.features.words_feature import WordsPresence as LegacyWordsPresence


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
        }
    )


@pytest.fixture
def sample_dataset(sample_data):
    return Dataset.from_pandas(sample_data)


@pytest.mark.parametrize("case_sensitive", [True, False])
@pytest.mark.parametrize("mode", ["any", "all"])
def test_contains_parameters(sample_dataset, case_sensitive, mode):
    legacy_feature = LegacyContains(
        column_name="description", items=["urgent", "important"], case_sensitive=case_sensitive, mode=mode
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = Contains(
        column_name="description", items=["urgent", "important"], case_sensitive=case_sensitive, mode=mode
    )

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


def test_contains_single_item(sample_dataset):
    legacy_feature = LegacyContains(column_name="description", items=["urgent"], case_sensitive=False)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = Contains(column_name="description", items=["urgent"], case_sensitive=False)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("case_sensitive", [True, False])
@pytest.mark.parametrize("mode", ["any", "all"])
def test_does_not_contain_parameters(sample_dataset, case_sensitive, mode):
    legacy_feature = LegacyDoesNotContain(
        column_name="description", items=["spam", "test"], case_sensitive=case_sensitive, mode=mode
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = DoesNotContain(
        column_name="description", items=["spam", "test"], case_sensitive=case_sensitive, mode=mode
    )

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("case_sensitive", [True, False])
@pytest.mark.parametrize("mode", ["any", "all"])
def test_item_match_parameters(sample_dataset, case_sensitive, mode):
    legacy_feature = LegacyItemMatch(columns=["description", "keywords"], case_sensitive=case_sensitive, mode=mode)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = ItemMatch(columns=["description", "keywords"], case_sensitive=case_sensitive, mode=mode)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


def test_item_match_error_handling():
    with pytest.raises(ValueError, match="ItemMatch requires exactly 2 columns"):
        ItemMatch(columns=["single_column"])

    with pytest.raises(ValueError, match="ItemMatch requires exactly 2 columns"):
        ItemMatch(columns=["col1", "col2", "col3"])


@pytest.mark.parametrize("case_sensitive", [True, False])
@pytest.mark.parametrize("mode", ["any", "all"])
def test_item_no_match_parameters(sample_dataset, case_sensitive, mode):
    legacy_feature = LegacyItemNoMatch(columns=["description", "keywords"], case_sensitive=case_sensitive, mode=mode)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = ItemNoMatch(columns=["description", "keywords"], case_sensitive=case_sensitive, mode=mode)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("mode", ["includes_any", "includes_all", "excludes_any", "excludes_all"])
@pytest.mark.parametrize("lemmatize", [True, False])
def test_words_presence_parameters(sample_dataset, mode, lemmatize):
    legacy_feature = LegacyWordsPresence(
        column_name="description", words_list=["urgent", "important"], mode=mode, lemmatize=lemmatize
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = WordsPresence(
        column_name="description", words_list=["urgent", "important"], mode=mode, lemmatize=lemmatize
    )

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("mode", ["any", "all"])
@pytest.mark.parametrize("lemmatize", [True, False])
def test_includes_words_parameters(sample_dataset, mode, lemmatize):
    legacy_feature = LegacyIncludesWords(
        column_name="description", words_list=["urgent", "important"], mode=mode, lemmatize=lemmatize
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = IncludesWords(
        column_name="description", words_list=["urgent", "important"], mode=mode, lemmatize=lemmatize
    )

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("mode", ["any", "all"])
@pytest.mark.parametrize("lemmatize", [True, False])
def test_excludes_words_parameters(sample_dataset, mode, lemmatize):
    legacy_feature = LegacyExcludesWords(
        column_name="description", words_list=["spam", "test"], mode=mode, lemmatize=lemmatize
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = ExcludesWords(column_name="description", words_list=["spam", "test"], mode=mode, lemmatize=lemmatize)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("mode", ["any", "all"])
@pytest.mark.parametrize("lemmatize", [True, False])
def test_word_match_parameters(sample_dataset, mode, lemmatize):
    legacy_feature = LegacyWordMatch(columns=["description", "keywords"], mode=mode, lemmatize=lemmatize)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = WordMatch(columns=["description", "keywords"], mode=mode, lemmatize=lemmatize)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("mode", ["any", "all"])
@pytest.mark.parametrize("lemmatize", [True, False])
def test_word_no_match_parameters(sample_dataset, mode, lemmatize):
    legacy_feature = LegacyWordNoMatch(columns=["description", "keywords"], mode=mode, lemmatize=lemmatize)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = WordNoMatch(columns=["description", "keywords"], mode=mode, lemmatize=lemmatize)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


@pytest.mark.parametrize("lemmatize", [True, False])
def test_trigger_words_present_parameters(sample_dataset, lemmatize):
    legacy_feature = LegacyTriggerWordsPresent(
        column_name="description", words_list=["urgent", "important"], lemmatize=lemmatize
    )
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = TriggerWordsPresent(column_name="description", words_list=["urgent", "important"], lemmatize=lemmatize)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


def test_regex_parameters(sample_dataset):
    legacy_feature = LegacyRegExp(column_name="description", reg_exp=r".*(urgent|important).*")
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = RegExp(column_name="description", reg_exp=r".*(urgent|important).*")

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.astype(bool).tolist()


def test_single_item_list(sample_dataset):
    legacy_feature = LegacyContains(column_name="description", items=["urgent"], case_sensitive=False)
    legacy_desc = FeatureDescriptor(feature=legacy_feature)

    new_desc = Contains(column_name="description", items=["urgent"], case_sensitive=False)

    sample_dataset.add_descriptor(legacy_desc)
    sample_dataset.add_descriptor(new_desc)

    legacy_result = sample_dataset.column(legacy_desc.alias)
    new_result = sample_dataset.column(new_desc.alias)

    assert new_result.data.tolist() == legacy_result.data.tolist()


def test_contains_alias():
    desc = Contains("description", ["urgent", "important"])
    assert desc.alias is not None
    assert "description" in desc.alias


def test_does_not_contain_alias():
    desc = DoesNotContain("description", ["spam", "test"])
    assert desc.alias is not None
    assert "description" in desc.alias


def test_item_match_alias():
    desc = ItemMatch(["description", "keywords"])
    assert desc.alias is not None
    assert "description" in desc.alias
    assert "keywords" in desc.alias


def test_custom_alias_preservation():
    custom_alias = "custom_contains"
    desc = Contains("description", ["urgent"], alias=custom_alias)
    assert desc.alias == custom_alias
