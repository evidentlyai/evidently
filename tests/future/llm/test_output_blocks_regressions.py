import json

import pytest

from evidently.llm.utils.blocks import JsonOutputFormatBlock
from evidently.llm.utils.blocks import find_largest_json


@pytest.mark.parametrize(
    "payload",
    [
        {"outer": {"middle": {"inner": "value"}}},
        {"message": "a } brace and a { brace", "other": 'quoted "value"'},
    ],
)
def test_json_substring_parser_preserves_complete_objects(payload):
    response = "Explanation first.\n```json\n" + json.dumps(payload) + "\n```"
    assert find_largest_json(response) == payload
    assert JsonOutputFormatBlock(fields={}).parse_response(response) == payload


def test_json_substring_parser_selects_largest_object_and_skips_invalid_braces():
    response = 'invalid {text} then {"a": 1} then {"outer": {"inner": {"value": 2}}}'
    assert find_largest_json(response) == {"outer": {"inner": {"value": 2}}}
    assert find_largest_json("no JSON {oops}") is None
