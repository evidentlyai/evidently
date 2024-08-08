import json
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import pytest

from evidently.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.features.llm_judge import LLMResponseParseError


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
