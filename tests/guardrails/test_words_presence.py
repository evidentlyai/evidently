import pytest

from evidently.guardrails import WordsPresence
from evidently.guardrails.core import GuardException


@pytest.mark.parametrize(
    "data,words,presence_mode,search_mode,lemmatize,expected",
    [
        ("Some words", ["some"], "includes", "all", False, "pass"),
        ("Some words", ["any"], "includes", "all", False, "fail"),
        ("Some words", ["some", "any"], "includes", "any", False, "pass"),
        ("Some words", ["another", "any"], "includes", "any", False, "fail"),
        ("Some words", ["some"], "excludes", "all", False, "fail"),
        ("Some words", ["any"], "excludes", "all", False, "pass"),
        ("Some words", ["some", "any"], "excludes", "any", False, "pass"),
        ("Some words", ["another", "any"], "excludes", "any", False, "pass"),
        ("Some words", ["word"], "includes", "all", True, "pass"),
    ],
)
def test_words_presence_guards_passed(data, words, presence_mode, search_mode, lemmatize, expected):
    if expected == "pass":
        WordsPresence(words, presence_mode, search_mode, lemmatize).validate(data)
    if expected == "fail":
        with pytest.raises(GuardException):
            WordsPresence(words, presence_mode, search_mode, lemmatize).validate(data)
