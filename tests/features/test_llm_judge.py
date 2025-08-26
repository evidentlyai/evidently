import json
import re
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import pytest

from evidently.legacy.descriptors import NegativityLLMEval
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.legacy.features.llm_judge import LLMJudge
from evidently.legacy.features.llm_judge import LLMMessage
from evidently.legacy.features.llm_judge import LLMWrapper
from evidently.legacy.metric_preset import TextEvals
from evidently.legacy.options.base import Options
from evidently.legacy.report import Report
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.llm.errors import LLMResponseParseError
from evidently.legacy.utils.llm.wrapper import LLMResult
from evidently.legacy.utils.llm.wrapper import llm_provider


def _LLMPromptTemplate(
    include_reasoning: bool,
    target_category: str,
    non_target_category: str,
    score_range: Optional[Tuple[float, float]] = None,
):
    return BinaryClassificationPromptTemplate(
        criteria="",
        instructions_template="",
        include_reasoning=include_reasoning,
        target_category=target_category,
        non_target_category=non_target_category,
        include_score=score_range is not None,
        score_range=score_range or (0, 1),
    )


@pytest.mark.parametrize(
    "template,results",
    [
        (
            _LLMPromptTemplate(include_reasoning=False, target_category="FIRST", non_target_category="SECOND"),
            {
                json.dumps({"result": "FIRST"}): {"result": "FIRST"},
                json.dumps({"result": "SECOND"}): {"result": "SECOND"},
            },
        ),
        (
            _LLMPromptTemplate(include_reasoning=True, target_category="FIRST", non_target_category="SECOND"),
            {
                json.dumps({"result": "FIRST", "reasoning": "Reason"}): {"result": "FIRST", "reasoning": "Reason"},
                json.dumps({"result": "SECOND", "reasoning": "Reason"}): {"result": "SECOND", "reasoning": "Reason"},
            },
        ),
        (
            _LLMPromptTemplate(
                include_reasoning=False, target_category="FIRST", non_target_category="SECOND", score_range=(0, 1)
            ),
            {
                json.dumps({"result": 0}): {"result": 0},
                json.dumps({"result": 1}): {"result": 1},
            },
        ),
        (
            _LLMPromptTemplate(
                include_reasoning=True, target_category="FIRST", non_target_category="SECOND", score_range=(0, 1)
            ),
            {
                json.dumps({"result": 0, "reasoning": "Reason"}): {"result": 0, "reasoning": "Reason"},
                json.dumps({"result": 1, "reasoning": "Reason"}): {"result": 1, "reasoning": "Reason"},
            },
        ),
    ],
)
def test_parse_response(
    template: BinaryClassificationPromptTemplate,
    results: Dict[str, Union[LLMResponseParseError, Dict[str, Union[str, float]]]],
):
    for response, expected_result in results.items():
        if isinstance(expected_result, LLMResponseParseError):
            with pytest.raises(expected_result.__class__):
                template.get_parser()(response)
        else:
            assert template.get_parser()(response) == expected_result


@llm_provider("mock", None)
class MockLLMWrapper(LLMWrapper):
    def __init__(self, model: str, options: Options):
        self.model = model

    async def complete(self, messages: List[LLMMessage], seed: Optional[int] = None) -> LLMResult[str]:
        text = messages[-1].content
        cat = re.findall("___text_starts_here___\n(.*)\n___text_ends_here___", text)[0][0]
        return LLMResult(json.dumps({"category": cat}), 0, 0)


@pytest.mark.asyncio
def test_llm_judge():
    llm_judge = LLMJudge(
        input_column="text",
        provider="mock",
        model="",
        template=BinaryClassificationPromptTemplate(target_category="A", non_target_category="B"),
    )

    data = pd.DataFrame({"text": ["A", "B"]})

    dd = DataDefinition(columns={}, reference_present=False)
    fts = llm_judge.generate_features(data, dd, Options())
    pd.testing.assert_frame_equal(fts, pd.DataFrame({"category": ["A", "B"]}))


@pytest.mark.asyncio
def test_multicol_llm_judge():
    llm_judge = LLMJudge(
        input_columns={"text": "input", "text2": "input2"},
        provider="mock",
        model="",
        template=BinaryClassificationPromptTemplate(target_category="A", non_target_category="B"),
    )

    data = pd.DataFrame({"text": ["A", "B"], "text2": ["C", "D"]})

    dd = DataDefinition(columns={}, reference_present=False)
    fts = llm_judge.generate_features(data, dd, Options())
    pd.testing.assert_frame_equal(fts, pd.DataFrame({"category": ["A", "B"]}))


def test_run_snapshot_with_llm_judge():
    data = pd.DataFrame({"text": ["A", "B"], "text2": ["C", "D"]})
    neg_eval = NegativityLLMEval(
        input_columns={"text": "input", "text2": "input2"},
        provider="mock",
        model="",
        template=BinaryClassificationPromptTemplate(target_category="A", non_target_category="B"),
    )
    report = Report(metrics=[TextEvals("text", descriptors=[neg_eval])])

    report.run(current_data=data, reference_data=None)
    report._inner_suite.raise_for_error()
    assert report.as_dict() == {
        "metrics": [
            {
                "metric": "ColumnSummaryMetric",
                "result": {
                    "column_name": "Negativity",
                    "column_type": "cat",
                    "current_characteristics": {
                        "count": 2,
                        "missing": 0,
                        "missing_percentage": 0.0,
                        "most_common": "A",
                        "most_common_percentage": 50.0,
                        "new_in_current_values_count": None,
                        "number_of_rows": 2,
                        "unique": 2,
                        "unique_percentage": 100.0,
                        "unused_in_current_values_count": None,
                    },
                    "reference_characteristics": None,
                },
            }
        ]
    }
