import json
import re
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import pytest

from evidently.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.features.llm_judge import LLMJudge
from evidently.features.llm_judge import LLMMessage
from evidently.features.llm_judge import LLMResponseParseError
from evidently.features.llm_judge import LLMWrapper
from evidently.features.llm_judge import llm_provider
from evidently.options.base import Options
from evidently.utils.data_preprocessing import DataDefinition


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
    template: _LLMPromptTemplate, results: Dict[str, Union[LLMResponseParseError, Dict[str, Union[str, float]]]]
):
    for response, expected_result in results.items():
        if isinstance(expected_result, LLMResponseParseError):
            with pytest.raises(expected_result.__class__):
                template.parse_response(response)
        else:
            assert template.parse_response(response) == expected_result


@llm_provider("mock", None)
class MockLLMWrapper(LLMWrapper):
    def __init__(self, model: str, options: Options):
        self.model = model

    def complete(self, messages: List[LLMMessage]) -> str:
        text = messages[-1][1]
        cat = re.findall("___text_starts_here___\n(.*)\n___text_ends_here___", text)[0][0]
        return json.dumps({"category": cat})


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
