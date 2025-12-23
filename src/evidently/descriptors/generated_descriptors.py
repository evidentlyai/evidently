from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from evidently.core.datasets import DescriptorTest
from evidently.core.datasets import FeatureDescriptor
from evidently.core.tests import GenericTest
from evidently.legacy.core import ColumnType
from evidently.legacy.features.llm_judge import BaseLLMPromptTemplate
from evidently.legacy.features.llm_judge import Uncertainty


def BERTScore(
    columns: List[str],
    model: str = "bert-base-uncased",
    tfidf_weighted: bool = False,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Compute BERTScore similarity between text columns.

    Args:
    * `columns`: List of column names to compare.
    * `model`: Pretrained BERT model name.
    * `tfidf_weighted`: Whether to weight embeddings with IDF.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.BERTScore_feature import BERTScoreFeature as BERTScoreFeatureV1

    feature = BERTScoreFeatureV1(columns=columns, model=model, tfidf_weighted=tfidf_weighted, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def BeginsWith(
    column_name: str,
    prefix: str,
    case_sensitive: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column values begin with the specified prefix.

    Args:
    * `column_name`: Name of the text column to check.
    * `prefix`: Prefix string to match.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_part_feature import BeginsWith as BeginsWithV1

    feature = BeginsWithV1(column_name=column_name, prefix=prefix, case_sensitive=case_sensitive, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def Contains(
    column_name: str,
    items: List[str],
    case_sensitive: bool = True,
    mode: str = "any",
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column contains any or all of the specified items.

    Args:
    * `column_name`: Name of the text column to check.
    * `items`: List of strings to search for.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `mode`: Matching mode: "any" or "all".
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_contains_feature import Contains as ContainsV1

    feature = ContainsV1(
        column_name=column_name, items=items, case_sensitive=case_sensitive, mode=mode, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ContainsLink(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Check if text column contains URLs or links.

    Args:
    * `column_name`: Name of the text column to check.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.contains_link_feature import ContainsLink as ContainsLinkV1

    feature = ContainsLinkV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def DoesNotContain(
    column_name: str,
    items: List[str],
    case_sensitive: bool = True,
    mode: str = "any",
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column does not contain specified items.

    Args:
    * `column_name`: Name of the text column to check.
    * `items`: List of strings to search for.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `mode`: Matching mode: "any" or "all".
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_contains_feature import DoesNotContain as DoesNotContainV1

    feature = DoesNotContainV1(
        column_name=column_name, items=items, case_sensitive=case_sensitive, mode=mode, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def EndsWith(
    column_name: str,
    suffix: str,
    case_sensitive: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column values end with the specified suffix.

    Args:
    * `column_name`: Name of the text column to check.
    * `suffix`: Suffix string to match.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_part_feature import EndsWith as EndsWithV1

    feature = EndsWithV1(column_name=column_name, suffix=suffix, case_sensitive=case_sensitive, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ExactMatch(
    columns: List[str],
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if multiple columns have exactly matching values.

    Args:
    * `columns`: List of column names to compare.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.exact_match_feature import ExactMatchFeature as ExactMatchFeatureV1

    feature = ExactMatchFeatureV1(columns=columns, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ExcludesWords(
    column_name: str,
    words_list: List[str],
    mode: str = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column excludes specified words.

    Args:
    * `column_name`: Name of the text column to check.
    * `words_list`: List of words to check for exclusion.
    * `mode`: Matching mode: "any" or "all".
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.words_feature import ExcludesWords as ExcludesWordsV1

    feature = ExcludesWordsV1(
        column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def HuggingFace(
    column_name: str,
    model: str,
    params: dict,
    alias: str,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Apply a HuggingFace model to text column.

    Args:
    * `column_name`: Name of the text column to process.
    * `model`: HuggingFace model name or path.
    * `params`: Additional parameters for the model.
    * `alias`: Alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.hf_feature import HuggingFaceFeature as HuggingFaceFeatureV1

    feature = HuggingFaceFeatureV1(column_name=column_name, model=model, params=params, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def HuggingFaceToxicity(
    column_name: str,
    alias: str,
    model: Optional[str] = None,
    toxic_label: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Detect toxicity in text using HuggingFace models.

    Args:
    * `column_name`: Name of the text column to check.
    * `alias`: Alias for the descriptor.
    * `model`: HuggingFace model name or path. If None, uses default.
    * `toxic_label`: Label to use for toxic predictions.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.hf_feature import HuggingFaceToxicityFeature as HuggingFaceToxicityFeatureV1

    feature = HuggingFaceToxicityFeatureV1(
        column_name=column_name, model=model, toxic_label=toxic_label, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def IncludesWords(
    column_name: str,
    words_list: List[str],
    mode: str = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text column includes specified words.

    Args:
    * `column_name`: Name of the text column to check.
    * `words_list`: List of words to search for.
    * `mode`: Matching mode: "any" or "all".
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.words_feature import IncludesWords as IncludesWordsV1

    feature = IncludesWordsV1(
        column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def IsValidJSON(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Check if text column contains valid JSON.

    Args:
    * `column_name`: Name of the text column to validate.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.is_valid_json_feature import IsValidJSON as IsValidJSONV1

    feature = IsValidJSONV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def IsValidPython(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Check if text column contains valid Python code.

    Args:
    * `column_name`: Name of the text column to validate.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.is_valid_python_feature import IsValidPython as IsValidPythonV1

    feature = IsValidPythonV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def IsValidSQL(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Check if text column contains valid SQL.

    Args:
    * `column_name`: Name of the text column to validate.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.is_valid_sql_feature import IsValidSQL as IsValidSQLV1

    feature = IsValidSQLV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ItemMatch(
    columns: List[str],
    case_sensitive: bool = True,
    mode: str = "any",
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if items from one column match items in another column.

    Args:
    * `columns`: List of two column names to compare.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `mode`: Matching mode: "any" or "all".
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_contains_feature import ItemMatch as ItemMatchV1

    feature = ItemMatchV1(columns=columns, case_sensitive=case_sensitive, mode=mode, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ItemNoMatch(
    columns: List[str],
    case_sensitive: bool = True,
    mode: str = "any",
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if items from one column do not match items in another column.

    Args:
    * `columns`: List of two column names to compare.
    * `case_sensitive`: Whether matching is case-sensitive.
    * `mode`: Matching mode: "any" or "all".
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.text_contains_feature import ItemNoMatch as ItemNoMatchV1

    feature = ItemNoMatchV1(columns=columns, case_sensitive=case_sensitive, mode=mode, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def JSONMatch(
    first_column: str,
    second_column: str,
    feature_type: ColumnType = ColumnType.Categorical,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if JSON values in two columns match.

    Args:
    * `first_column`: Name of the first JSON column.
    * `second_column`: Name of the second JSON column.
    * `feature_type`: Type of the output feature.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.json_match_feature import JSONMatch as JSONMatchV1

    feature = JSONMatchV1(
        first_column=first_column, second_column=second_column, feature_type=feature_type, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def JSONSchemaMatch(
    column_name: str,
    expected_schema: Dict[str, Type],
    validate_types: bool = False,
    exact_match: bool = False,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if JSON values match the expected schema.

    Args:
    * `column_name`: Name of the JSON column to validate.
    * `expected_schema`: Dictionary mapping field names to expected types.
    * `validate_types`: Whether to validate field types.
    * `exact_match`: Whether schema must match exactly.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.json_schema_match_feature import JSONSchemaMatch as JSONSchemaMatchV1

    feature = JSONSchemaMatchV1(
        column_name=column_name,
        expected_schema=expected_schema,
        validate_types=validate_types,
        exact_match=exact_match,
        display_name=alias,
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def LLMJudge(
    provider: str,
    model: str,
    template: BaseLLMPromptTemplate,
    input_column: Optional[str] = None,
    input_columns: Optional[Dict[str, str]] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate text using LLM with a custom prompt template.

    Args:
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `template`: Prompt template defining the evaluation task.
    * `input_column`: Single input column name (if using single column).
    * `input_columns`: Mapping of prompt variables to column names (if using multiple columns).
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.llm_judge import LLMJudge as LLMJudgeV1

    feature = LLMJudgeV1(
        provider=provider,
        model=model,
        template=template,
        input_column=input_column,
        input_columns=input_columns,
        display_name=alias,
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def NonLetterCharacterPercentage(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Compute percentage of non-letter characters in text.

    Args:
    * `column_name`: Name of the text column to analyze.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.non_letter_character_percentage_feature import (
        NonLetterCharacterPercentage as NonLetterCharacterPercentageV1,
    )

    feature = NonLetterCharacterPercentageV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def OOVWordsPercentage(
    column_name: str,
    ignore_words: Any = (),
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Compute percentage of out-of-vocabulary words in text.

    Args:
    * `column_name`: Name of the text column to analyze.
    * `ignore_words`: Words to ignore when computing OOV percentage.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.OOV_words_percentage_feature import OOVWordsPercentage as OOVWordsPercentageV1

    feature = OOVWordsPercentageV1(column_name=column_name, ignore_words=ignore_words, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def OpenAI(
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
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate text using OpenAI models with custom prompts.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `model`: OpenAI model name to use.
    * `prompt`: Prompt template string.
    * `feature_type`: Type of output feature.
    * `context`: Optional context string.
    * `context_column`: Optional column name containing context.
    * `prompt_replace_string`: String to replace in prompt with column value.
    * `context_replace_string`: String to replace in prompt with context.
    * `check_mode`: Mode for checking results: "any_line" or other modes.
    * `possible_values`: Optional list of possible output values.
    * `openai_params`: Optional dictionary of additional OpenAI API parameters.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.openai_feature import OpenAIFeature as OpenAIFeatureV1

    feature = OpenAIFeatureV1(
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
        display_name=alias,
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def RegExp(
    column_name: str,
    reg_exp: str,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if text matches a regular expression pattern.

    Args:
    * `column_name`: Name of the text column to check.
    * `reg_exp`: Regular expression pattern to match.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.regexp_feature import RegExp as RegExpV1

    feature = RegExpV1(column_name=column_name, reg_exp=reg_exp, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def SemanticSimilarity(
    columns: List[str],
    model: str = "all-MiniLM-L6-v2",
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Compute semantic similarity between text columns.

    Args:
    * `columns`: List of column names to compare.
    * `model`: Sentence transformer model name.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.semantic_similarity_feature import (
        SemanticSimilarityFeature as SemanticSimilarityFeatureV1,
    )

    feature = SemanticSimilarityFeatureV1(columns=columns, model=model, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def SentenceCount(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Count the number of sentences in text.

    Args:
    * `column_name`: Name of the text column to analyze.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.sentence_count_feature import SentenceCount as SentenceCountV1

    feature = SentenceCountV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def Sentiment(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Compute sentiment score for text.

    Args:
    * `column_name`: Name of the text column to analyze.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.sentiment_feature import Sentiment as SentimentV1

    feature = SentimentV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def TriggerWordsPresent(
    column_name: str,
    words_list: List[str],
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if trigger words are present in text.

    Args:
    * `column_name`: Name of the text column to check.
    * `words_list`: List of trigger words to search for.
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.trigger_words_presence_feature import TriggerWordsPresent as TriggerWordsPresentV1

    feature = TriggerWordsPresentV1(
        column_name=column_name, words_list=words_list, lemmatize=lemmatize, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def WordCount(
    column_name: str, alias: Optional[str] = None, tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None
):
    """Count the number of words in text.

    Args:
    * `column_name`: Name of the text column to analyze.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.word_count_feature import WordCount as WordCountV1

    feature = WordCountV1(column_name=column_name, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def WordMatch(
    columns: List[str],
    mode: str,
    lemmatize: bool,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if words from one column match words in another column.

    Args:
    * `columns`: List of two column names to compare.
    * `mode`: Matching mode: "any" or "all".
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.words_feature import WordMatch as WordMatchV1

    feature = WordMatchV1(columns=columns, mode=mode, lemmatize=lemmatize, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def WordNoMatch(
    columns: List[str],
    mode: str,
    lemmatize: bool,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check if words from one column do not match words in another column.

    Args:
    * `columns`: List of two column names to compare.
    * `mode`: Matching mode: "any" or "all".
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.words_feature import WordNoMatch as WordNoMatchV1

    feature = WordNoMatchV1(columns=columns, mode=mode, lemmatize=lemmatize, display_name=alias)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def WordsPresence(
    column_name: str,
    words_list: List[str],
    mode: str = "includes_any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Check presence of words in text with various matching modes.

    Args:
    * `column_name`: Name of the text column to check.
    * `words_list`: List of words to search for.
    * `mode`: Matching mode: "includes_any", "includes_all", "excludes_any", or "excludes_all".
    * `lemmatize`: Whether to lemmatize words before matching.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.features.words_feature import WordsPresence as WordsPresenceV1

    feature = WordsPresenceV1(
        column_name=column_name, words_list=words_list, mode=mode, lemmatize=lemmatize, display_name=alias
    )
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def BiasLLMEval(
    column_name: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate bias in text using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import BiasLLMEval as BiasLLMEvalV1

    feature = BiasLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def BinaryClassificationLLMEval(
    column_name: str,
    provider: str,
    model: str,
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Perform binary classification evaluation using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import BinaryClassificationLLMEval as BinaryClassificationLLMEvalV1

    feature = BinaryClassificationLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def CompletenessLLMEval(
    column_name: str,
    context: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate completeness of text against context using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `context`: Column name containing context for evaluation.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import CompletenessLLMEval as CompletenessLLMEvalV1

    feature = CompletenessLLMEvalV1(
        context=context,
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ContextQualityLLMEval(
    column_name: str,
    question: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate quality of context for answering a question using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `question`: Column name containing question for evaluation.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import ContextQualityLLMEval as ContextQualityLLMEvalV1

    feature = ContextQualityLLMEvalV1(
        question=question,
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def CorrectnessLLMEval(
    column_name: str,
    target_output: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate correctness of text against target output using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `target_output`: Column name containing target output for comparison.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import CorrectnessLLMEval as CorrectnessLLMEvalV1

    feature = CorrectnessLLMEvalV1(
        target_output=target_output,
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def DeclineLLMEval(
    column_name: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Detect if LLM declined to answer using LLM evaluation.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import DeclineLLMEval as DeclineLLMEvalV1

    feature = DeclineLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def FaithfulnessLLMEval(
    column_name: str,
    context: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate faithfulness of text to context using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `context`: Column name containing context for evaluation.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import FaithfulnessLLMEval as FaithfulnessLLMEvalV1

    feature = FaithfulnessLLMEvalV1(
        context=context,
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def LLMEval(
    column_name: str,
    provider: str,
    model: str,
    template: BaseLLMPromptTemplate,
    additional_columns: Optional[Dict[str, str]] = None,
    subcolumn: Optional[str] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate text using LLM with a custom prompt template.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `template`: Prompt template defining the evaluation task.
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `subcolumn`: Optional subcolumn name for nested data.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import LLMEval as LLMEvalV1

    feature = LLMEvalV1(
        provider=provider,
        model=model,
        template=template,
        additional_columns=additional_columns,
        subcolumn=subcolumn,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def MulticlassClassificationLLMEval(
    column_name: str,
    provider: str,
    model: str,
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Perform multiclass classification evaluation using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import (
        MulticlassClassificationLLMEval as MulticlassClassificationLLMEvalV1,
    )

    feature = MulticlassClassificationLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def NegativityLLMEval(
    column_name: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate negativity in text using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import NegativityLLMEval as NegativityLLMEvalV1

    feature = NegativityLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def PIILLMEval(
    column_name: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Detect personally identifiable information in text using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import PIILLMEval as PIILLMEvalV1

    feature = PIILLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)


def ToxicityLLMEval(
    column_name: str,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    additional_columns: Optional[Dict[str, str]] = None,
    include_category: Optional[bool] = None,
    include_score: Optional[bool] = None,
    include_reasoning: Optional[bool] = None,
    uncertainty: Optional[Uncertainty] = None,
    alias: Optional[str] = None,
    tests: Optional[List[Union["DescriptorTest", "GenericTest"]]] = None,
):
    """Evaluate toxicity in text using LLM.

    Args:
    * `column_name`: Name of the text column to evaluate.
    * `provider`: LLM provider name (e.g., "openai", "anthropic").
    * `model`: Model name to use (e.g., "gpt-4o-mini").
    * `additional_columns`: Optional mapping of prompt variables to column names.
    * `include_category`: Whether to include category in output.
    * `include_score`: Whether to include score in output.
    * `include_reasoning`: Whether to include reasoning in output.
    * `uncertainty`: Optional uncertainty handling strategy.
    * `alias`: Optional alias for the descriptor.
    * `tests`: Optional list of tests to apply.
    """
    from evidently.legacy.descriptors.llm_judges import ToxicityLLMEval as ToxicityLLMEvalV1

    feature = ToxicityLLMEvalV1(
        provider=provider,
        model=model,
        additional_columns=additional_columns,
        include_category=include_category,
        include_score=include_score,
        include_reasoning=include_reasoning,
        uncertainty=uncertainty,
        display_name=alias,
    ).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)
