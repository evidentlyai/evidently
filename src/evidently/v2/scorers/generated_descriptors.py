from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.core import ColumnType
from evidently.features.BERTScore_feature import BERTScoreFeature
from evidently.features.contains_link_feature import ContainsLink
from evidently.features.exact_match_feature import ExactMatchFeature
from evidently.features.hf_feature import HuggingFaceFeature
from evidently.features.hf_feature import HuggingFaceToxicityFeature
from evidently.features.is_valid_json_feature import IsValidJSON
from evidently.features.is_valid_python_feature import IsValidPython
from evidently.features.is_valid_sql_feature import IsValidSQL
from evidently.features.json_match_feature import JSONMatch
from evidently.features.json_schema_match_feature import JSONSchemaMatch
from evidently.features.llm_judge import BaseLLMPromptTemplate
from evidently.features.llm_judge import LLMJudge
from evidently.features.non_letter_character_percentage_feature import NonLetterCharacterPercentage
from evidently.features.OOV_words_percentage_feature import OOVWordsPercentage
from evidently.features.openai_feature import OpenAIFeature
from evidently.features.regexp_feature import RegExp
from evidently.features.semantic_similarity_feature import SemanticSimilarityFeature
from evidently.features.sentence_count_feature import SentenceCount
from evidently.features.sentiment_feature import Sentiment
from evidently.features.text_contains_feature import Contains
from evidently.features.text_contains_feature import DoesNotContain
from evidently.features.text_contains_feature import ItemMatch
from evidently.features.text_contains_feature import ItemNoMatch
from evidently.features.text_length_feature import TextLength
from evidently.features.text_part_feature import BeginsWith
from evidently.features.text_part_feature import EndsWith
from evidently.features.trigger_words_presence_feature import TriggerWordsPresent
from evidently.features.word_count_feature import WordCount
from evidently.features.words_feature import ExcludesWords
from evidently.features.words_feature import IncludesWords
from evidently.features.words_feature import WordMatch
from evidently.features.words_feature import WordNoMatch
from evidently.features.words_feature import WordsPresence
from evidently.v2.datasets import FeatureDescriptor


def bert_score(
    columns: List[str], model: str = "bert-base-uncased", tfidf_weighted: bool = False, alias: Optional[str] = None
):
    feature = BERTScoreFeature(columns=columns, model=model, tfidf_weighted=tfidf_weighted)
    return FeatureDescriptor(feature, alias=alias)


def begins_with(column_name: str, prefix: str, case_sensitive: bool = True, alias: Optional[str] = None):
    feature = BeginsWith(column_name=column_name, prefix=prefix, case_sensitive=case_sensitive)
    return FeatureDescriptor(feature, alias=alias)


def contains(
    column_name: str, items: List[str], case_sensitive: bool = True, mode: str = "any", alias: Optional[str] = None
):
    feature = Contains(column_name=column_name, items=items, case_sensitive=case_sensitive, mode=mode)
    return FeatureDescriptor(feature, alias=alias)


def contains_link(column_name: str, alias: Optional[str] = None):
    feature = ContainsLink(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def does_not_contain(
    column_name: str, items: List[str], case_sensitive: bool = True, mode: str = "any", alias: Optional[str] = None
):
    feature = DoesNotContain(column_name=column_name, items=items, case_sensitive=case_sensitive, mode=mode)
    return FeatureDescriptor(feature, alias=alias)


def ends_with(column_name: str, suffix: str, case_sensitive: bool = True, alias: Optional[str] = None):
    feature = EndsWith(column_name=column_name, suffix=suffix, case_sensitive=case_sensitive)
    return FeatureDescriptor(feature, alias=alias)


def exact_match(columns: List[str], alias: Optional[str] = None):
    feature = ExactMatchFeature(columns=columns)
    return FeatureDescriptor(feature, alias=alias)


def excludes_words(
    column_name: str, words_list: List[str], mode: str = "any", lemmatize: bool = True, alias: Optional[str] = None
):
    feature = ExcludesWords(column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)


def hugging_face(column_name: str, model: str, params: dict, display_name: str, alias: Optional[str] = None):
    feature = HuggingFaceFeature(column_name=column_name, model=model, params=params, display_name=display_name)
    return FeatureDescriptor(feature, alias=alias)


def hugging_face_toxicity(
    column_name: str,
    display_name: str,
    model: Optional[str] = None,
    toxic_label: Optional[str] = None,
    alias: Optional[str] = None,
):
    feature = HuggingFaceToxicityFeature(
        column_name=column_name, display_name=display_name, model=model, toxic_label=toxic_label
    )
    return FeatureDescriptor(feature, alias=alias)


def includes_words(
    column_name: str, words_list: List[str], mode: str = "any", lemmatize: bool = True, alias: Optional[str] = None
):
    feature = IncludesWords(column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)


def is_valid_json(column_name: str, alias: Optional[str] = None):
    feature = IsValidJSON(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def is_valid_python(column_name: str, alias: Optional[str] = None):
    feature = IsValidPython(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def is_valid_sql(column_name: str, alias: Optional[str] = None):
    feature = IsValidSQL(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def item_match(columns: List[str], case_sensitive: bool = True, mode: str = "any", alias: Optional[str] = None):
    feature = ItemMatch(columns=columns, case_sensitive=case_sensitive, mode=mode)
    return FeatureDescriptor(feature, alias=alias)


def item_no_match(columns: List[str], case_sensitive: bool = True, mode: str = "any", alias: Optional[str] = None):
    feature = ItemNoMatch(columns=columns, case_sensitive=case_sensitive, mode=mode)
    return FeatureDescriptor(feature, alias=alias)


def json_match(
    first_column: str,
    second_column: str,
    feature_type: ColumnType = ColumnType.Categorical,
    alias: Optional[str] = None,
):
    feature = JSONMatch(first_column=first_column, second_column=second_column, feature_type=feature_type)
    return FeatureDescriptor(feature, alias=alias)


def json_schema_match(
    column_name: str,
    expected_schema: Dict[str, type],
    validate_types: bool = False,
    exact_match: bool = False,
    alias: Optional[str] = None,
):
    feature = JSONSchemaMatch(
        column_name=column_name, expected_schema=expected_schema, validate_types=validate_types, exact_match=exact_match
    )
    return FeatureDescriptor(feature, alias=alias)


def llm_judge(
    provider: str,
    model: str,
    template: BaseLLMPromptTemplate,
    input_column: Optional[str] = None,
    input_columns: Optional[Dict[str, str]] = None,
    alias: Optional[str] = None,
):
    feature = LLMJudge(
        provider=provider, model=model, template=template, input_column=input_column, input_columns=input_columns
    )
    return FeatureDescriptor(feature, alias=alias)


def non_letter_character_percentage(column_name: str, alias: Optional[str] = None):
    feature = NonLetterCharacterPercentage(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def oov_words_percentage(column_name: str, ignore_words: Any = (), alias: Optional[str] = None):
    feature = OOVWordsPercentage(column_name=column_name, ignore_words=ignore_words)
    return FeatureDescriptor(feature, alias=alias)


def openai(
    column_name: str,
    model: str,
    prompt: str,
    feature_type: str,
    context: Optional[str] = None,
    context_column: Optional[str] = None,
    prompt_replace_string: str = "REPLACE",
    context_replace_string: str = "CONTEXT",
    check_mode: str = "any_line",
    possible_values: Optional[List[str]] = None,
    openai_params: Optional[dict] = None,
    alias: Optional[str] = None,
):
    feature = OpenAIFeature(
        column_name=column_name,
        model=model,
        prompt=prompt,
        feature_type=feature_type,
        context=context,
        context_column=context_column,
        prompt_replace_string=prompt_replace_string,
        context_replace_string=context_replace_string,
        check_mode=check_mode,
        possible_values=possible_values,
        openai_params=openai_params,
    )
    return FeatureDescriptor(feature, alias=alias)


def reg_exp(column_name: str, reg_exp: str, alias: Optional[str] = None):
    feature = RegExp(column_name=column_name, reg_exp=reg_exp)
    return FeatureDescriptor(feature, alias=alias)


def semantic_similarity(columns: List[str], model: str = "all-MiniLM-L6-v2", alias: Optional[str] = None):
    feature = SemanticSimilarityFeature(columns=columns, model=model)
    return FeatureDescriptor(feature, alias=alias)


def sentence_count(column_name: str, alias: Optional[str] = None):
    feature = SentenceCount(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def sentiment(column_name: str, alias: Optional[str] = None):
    feature = Sentiment(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def text_length(column_name: str, alias: Optional[str] = None):
    feature = TextLength(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def trigger_words_present(column_name: str, words_list: List[str], lemmatize: bool = True, alias: Optional[str] = None):
    feature = TriggerWordsPresent(column_name=column_name, words_list=words_list, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)


def word_count(column_name: str, alias: Optional[str] = None):
    feature = WordCount(column_name=column_name)
    return FeatureDescriptor(feature, alias=alias)


def word_match(columns: List[str], mode: str, lemmatize: bool, alias: Optional[str] = None):
    feature = WordMatch(columns=columns, mode=mode, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)


def word_no_match(columns: List[str], mode: str, lemmatize: bool, alias: Optional[str] = None):
    feature = WordNoMatch(columns=columns, mode=mode, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)


def words_presence(
    column_name: str, words_list: List[str], mode: str = "any", lemmatize: bool = True, alias: Optional[str] = None
):
    feature = WordsPresence(column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize)
    return FeatureDescriptor(feature, alias=alias)
