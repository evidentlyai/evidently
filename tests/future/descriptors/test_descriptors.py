import json
from inspect import isabstract
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import pytest

from evidently import ColumnType
from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import ColumnTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.core.datasets import FeatureDescriptor
from evidently.core.datasets import TestSummary
from evidently.descriptors import ContextRelevance
from evidently.descriptors import CustomColumnDescriptor
from evidently.descriptors import CustomDescriptor
from evidently.descriptors import LLMJudge
from evidently.descriptors import TextLength
from evidently.descriptors import TextMatch
from evidently.descriptors.llm_judges import GenericLLMDescriptor
from evidently.descriptors.llm_judges import LLMEval
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.llm.wrapper import LLMResult
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import llm_provider
from evidently.llm.prompts.content import TemplatePromptContent
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.llm.utils.blocks import PromptBlock
from evidently.tests import eq
from tests.conftest import load_all_subtypes

from .test_feature_descriptors import MockGeneratedFeature

int_data = pd.Series([1, 2, 3], name="int")
str_data = pd.Series(["a", "b", "c"], name="str")


@llm_provider("mock_d", None)
class MockLLMWrapper(LLMWrapper):
    def __init__(self, model: str, options: Options):
        self.model = model

    async def complete(self, messages: List[LLMMessage], seed: Optional[int] = None) -> LLMResult[str]:
        return LLMResult("\n".join(m.content for m in messages), 0, 0)


def custom_descr(dataset: Dataset) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, pd.Series([1] * len(dataset.as_dataframe())))


def custom_col_descr(col: DatasetColumn) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, col.data)


class MockTemplate(BaseLLMPromptTemplate):
    blocks: ClassVar = [PromptBlock.simple("{data}")]

    def list_output_columns(self) -> List[str]:
        return ["res"]

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        return ColumnType.Text

    def get_main_output_column(self) -> str:
        return "res"


class MockTemplateMulticolumn(BaseLLMPromptTemplate):
    blocks: ClassVar = [PromptBlock.simple("{data}"), PromptBlock.json_output(**{"res1": "", "res2": ""})]

    def list_output_columns(self) -> List[str]:
        return ["res1", "res2"]

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        return ColumnType.Text

    def get_main_output_column(self) -> str:
        return "res1"


@pytest.fixture(autouse=True)
def mock_semantic_scoring(mocker):
    from evidently.descriptors._context_relevance import MeanAggregation
    from evidently.descriptors._context_relevance import semantic_similarity_scoring as sss

    def semantic_scoring_mock(question: DatasetColumn, context: DatasetColumn, options) -> DatasetColumn:
        return DatasetColumn(ColumnType.Numerical, pd.Series([1] * len(question.data)))

    mocker.patch(f"{sss.__module__}.{sss.__name__}", new=semantic_scoring_mock)
    mocker.patch(
        f"{sss.__module__}.METHODS",
        new={
            "semantic_similarity": (semantic_scoring_mock, MeanAggregation),
        },
    )


all_descriptors: List[Tuple[Descriptor, Union[pd.Series, pd.DataFrame], Dict[str, pd.Series]]] = [
    (
        FeatureDescriptor(feature=MockGeneratedFeature(column="str", field="a"), alias="res"),
        str_data,
        {"a1702de9f83a993ea3cb4701ca9d17f7.str": pd.Series(["aa", "ba", "ca"])},
    ),
    (
        LLMJudge(provider="mock_d", model="", template=MockTemplate(), input_columns={"aaa": "data"}, alias="res"),
        pd.DataFrame({"aaa": ["x", "y"]}),
        {"res": pd.Series(["x", "y"])},
    ),
    (TextLength(column_name="str", alias="res"), str_data, {"res": pd.Series([1, 1, 1])}),
    (CustomColumnDescriptor(column_name="int", func=custom_col_descr, alias="res"), int_data, {"res": int_data}),
    (CustomDescriptor(func=custom_descr, alias="res"), int_data, {"res": pd.Series([1, 1, 1])}),
    (TestSummary(alias="res"), int_data, {"res": pd.Series([1, 0, 0])}),
    (
        ContextRelevance(alias="res", input="i", contexts="c"),
        pd.DataFrame({"i": ["input"], "c": ["context"]}),
        {"res": pd.Series([1])},
    ),
    (
        GenericLLMDescriptor(
            alias="res",
            provider="mock_d",
            model="",
            input_columns={"aaa": "data"},
            prompt=[{"role": "system", "content": "a"}, {"role": "user", "content": "{data}"}],
        ),
        pd.DataFrame({"aaa": ["x", "y"]}),
        {"res": pd.Series(["a\nx", "a\ny"])},
    ),
    (
        GenericLLMDescriptor(
            alias="res",
            provider="mock_d",
            model="",
            input_columns={"aaa": "data"},
            prompt=TemplatePromptContent(template=MockTemplate()),
        ),
        pd.DataFrame({"aaa": ["x", "y"]}),
        {"res": pd.Series(["x", "y"])},
    ),
    (
        GenericLLMDescriptor(
            alias="res",
            provider="mock_d",
            model="",
            input_columns={"aaa": "data"},
            prompt=TemplatePromptContent(template=MockTemplateMulticolumn()),
        ),
        pd.DataFrame(
            {
                "aaa": [
                    json.dumps({"res1": 1, "res2": "a"}),
                    json.dumps({"res1": 2, "res2": "b"}),
                ]
            }
        ),
        {
            "res res1": pd.Series([1, 2]),
            "res res2": pd.Series(["a", "b"]),
        },
    ),
    (
        LLMEval(
            alias="res",
            provider="mock_d",
            model="",
            input_columns={"aaa": "data"},
            template=MockTemplate(),
        ),
        pd.DataFrame({"aaa": ["x", "y"]}),
        {"res": pd.Series(["x", "y"])},
    ),
    (TextMatch(alias="res", column_name="str", match_items=["a"]), str_data, {"res": pd.Series([True, False, False])}),
]


def test_descriptors_tested():
    tested_desc_set = {type(p) for p, _, _ in all_descriptors}
    load_all_subtypes(Descriptor)
    all_desc_types = set(s for s in Descriptor.__subclasses__() if not isabstract(s))
    assert tested_desc_set == all_desc_types, "Missing tests for descriptors " + ", ".join(
        f'({t.__name__}(alias="res"), pd.Series(), {{"res":pd.Series()}})' for t in all_desc_types - tested_desc_set
    )


@pytest.mark.parametrize("descriptor,data,result", all_descriptors)
def test_descriptors(descriptor: Descriptor, data: Union[pd.Series, pd.DataFrame], result: Dict[str, pd.Series]):
    df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    if isinstance(descriptor, TestSummary):
        dataset.add_descriptor(ColumnTest(str(df.columns[0]), eq(1)))
    dataset.add_descriptor(descriptor)

    res_df = dataset.as_dataframe()
    for col, value in result.items():
        assert col in set(res_df.columns), f"no column {col}, cols: {res_df.columns}"
        assert res_df[col].tolist() == value.tolist()

    payload = json.loads(descriptor.json())
    descriptor2 = parse_obj_as(Descriptor, payload)
    assert descriptor2 == descriptor
