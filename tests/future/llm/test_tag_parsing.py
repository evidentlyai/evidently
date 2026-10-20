import pytest

from evidently.llm.utils.parsing import get_tag
from evidently.llm.utils.parsing import get_tags


@pytest.mark.parametrize("tag", ["answer.v1", "item+", "field[0]"])
def test_tag_parsers_treat_tag_names_literally(tag):
    response = f"<{tag}>first</{tag}>\n<{tag}>second</{tag}>"
    assert get_tag(response, tag) == "first"
    assert get_tags(response, tag) == ["first", "second"]


def test_tag_parsers_do_not_match_regex_lookalikes():
    response = "<answerXv1>wrong</answerXv1><answer.v1>right</answer.v1>"
    assert get_tag(response, "answer.v1") == "right"
    assert get_tags(response, "answer.v1") == ["right"]
