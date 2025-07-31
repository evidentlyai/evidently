import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import FeatureDescriptor
from evidently.descriptors import BeginsWith
from evidently.descriptors import BERTScore
from evidently.descriptors import BiasLLMEval
from evidently.descriptors import CompletenessLLMEval
from evidently.descriptors import Contains
from evidently.descriptors import ContainsLink
from evidently.descriptors import ContextQualityLLMEval
from evidently.descriptors import ContextRelevance
from evidently.descriptors import CorrectnessLLMEval
from evidently.descriptors import DeclineLLMEval
from evidently.descriptors import DoesNotContain
from evidently.descriptors import EndsWith
from evidently.descriptors import ExactMatch
from evidently.descriptors import ExcludesWords
from evidently.descriptors import FaithfulnessLLMEval
from evidently.descriptors import IncludesWords
from evidently.descriptors import IsValidJSON
from evidently.descriptors import IsValidPython
from evidently.descriptors import IsValidSQL
from evidently.descriptors import ItemMatch
from evidently.descriptors import ItemNoMatch
from evidently.descriptors import JSONMatch
from evidently.descriptors import JSONSchemaMatch
from evidently.descriptors import NegativityLLMEval
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import OOVWordsPercentage
from evidently.descriptors import PIILLMEval
from evidently.descriptors import RegExp
from evidently.descriptors import SemanticSimilarity
from evidently.descriptors import SentenceCount
from evidently.descriptors import Sentiment
from evidently.descriptors import TextLength
from evidently.descriptors import ToxicityLLMEval
from evidently.descriptors import TriggerWordsPresent
from evidently.descriptors import WordCount

descriptors = [
    BERTScore(columns=["col"]),
    BeginsWith(column_name="col", prefix="prefix_"),
    BiasLLMEval(column_name="col"),
    CompletenessLLMEval(column_name="col", context="context"),
    Contains(column_name="col", items=["item"]),
    ContainsLink(column_name="col"),
    ContextQualityLLMEval(column_name="col", question="question"),
    ContextRelevance(input="input", contexts="contexts"),
    CorrectnessLLMEval(column_name="col", target_output="target"),
    DeclineLLMEval(column_name="col"),
    DoesNotContain(column_name="col", items=["item"]),
    EndsWith(column_name="col", suffix="suffix"),
    ExactMatch(columns=["col", "col2"]),
    ExcludesWords(column_name="col", words_list=["and"]),
    FaithfulnessLLMEval(column_name="col", context="context"),
    IsValidSQL(column_name="col"),
    IsValidJSON(column_name="col"),
    IsValidPython(column_name="col"),
    ItemMatch(columns=["col", "col2"]),
    ItemNoMatch(columns=["col", "col2"]),
    JSONMatch(first_column="col", second_column="col2"),
    JSONSchemaMatch(column_name="col", expected_schema={}),
    NegativityLLMEval(column_name="col"),
    NonLetterCharacterPercentage(column_name="col"),
    OOVWordsPercentage(column_name="col"),
    PIILLMEval(column_name="col"),
    RegExp(column_name="col", reg_exp="."),
    SemanticSimilarity(columns=["col", "col2"]),
    SentenceCount(column_name="col"),
    Sentiment(column_name="col"),
    TextLength(column_name="col"),
    ToxicityLLMEval(column_name="col"),
    TriggerWordsPresent(column_name="col", words_list=["and"]),
    WordCount(column_name="col"),
    IncludesWords(column_name="col", words_list=["and"]),
]


@pytest.mark.parametrize(
    "descriptor",
    descriptors,
)
def test_serialization(descriptor):
    obj = descriptor.dict()
    parse_obj_as(FeatureDescriptor, obj)
