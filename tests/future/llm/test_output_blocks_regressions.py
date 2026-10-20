import json

import pytest

from evidently.llm.utils.blocks import JsonOutputFormatBlock
from evidently.llm.utils.blocks import find_largest_json
from evidently.llm.utils.prompt_render import PreparedTemplate


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


@pytest.mark.parametrize(
    "fields,expected",
    [
        ({"quality": 'Say "good"', "score": ("A score", "value")}, {"quality": 'Say "good"', "value": "A score"}),
        ({}, {}),
    ],
)
def test_json_output_example_is_valid_after_template_rendering(fields, expected):
    block = JsonOutputFormatBlock(fields=fields)
    prompt = PreparedTemplate(block.render(), output_format=block).render({})
    example = prompt[prompt.index("{") :]
    assert json.loads(example) == expected
