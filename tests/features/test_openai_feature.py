from typing import List
from typing import Optional

import pytest

from evidently.legacy.features.openai_feature import _postprocess_response


@pytest.mark.parametrize(
    ("response", "check_mode", "possible_values", "expected"),
    [
        # a label that is a substring of another label must not shadow it
        ("incorrect", "any_line_contains", ["correct", "incorrect"], "incorrect"),
        ("The answer is incorrect", "any_line_contains", ["correct", "incorrect"], "incorrect"),
        ("unclear\nincorrect", "any_line_contains", ["correct", "incorrect"], "incorrect"),
        # unaffected cases
        ("incorrect", "first_line_contains", ["incorrect", "correct"], "incorrect"),
        ("The answer is correct", "any_line_contains", ["correct", "incorrect"], "correct"),
        ("correct", "any_line_contains", ["incorrect", "correct"], "correct"),
        ("yes, no", "any_line_contains", ["yes", "no"], "yes"),
        # caller order still decides between labels that are not nested in each other
        ("YES NO", "any_line_contains", ["no", "yes"], "no"),
        # caller order also decides when both nested labels appear on their own
        ("correct and incorrect", "any_line_contains", ["correct", "incorrect"], "correct"),
        # a label that only appears inside a longer label is not a match
        ("cannot", "any_line_contains", ["no", "cannot"], "cannot"),
        ("incorrect", "any_line", ["correct", "incorrect"], "incorrect"),
        ("maybe", "any_line_contains", ["correct", "incorrect"], None),
    ],
)
def test_postprocess_response(response: str, check_mode: str, possible_values: List[str], expected: Optional[str]):
    assert _postprocess_response(response, check_mode, possible_values) == expected
