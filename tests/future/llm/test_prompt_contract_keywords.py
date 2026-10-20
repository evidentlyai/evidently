import pytest

from evidently.llm.utils.templates import StrPromptTemplate
from evidently.llm.utils.templates import prompt_contract


class KeywordPrompt(StrPromptTemplate):
    @prompt_contract
    def ask(self, *, question: str) -> str:
        """Question: {question}"""


def test_prompt_contract_accepts_keyword_only_placeholders():
    prompt = KeywordPrompt.compile("Question: {question}")
    request = prompt.ask(question="What is drift?")
    assert request.messages[0].content == "Question: What is drift?"
    assert request.response_parser("An answer") == "An answer"


def test_prompt_contract_still_rejects_missing_keyword_placeholders():
    with pytest.raises(ValueError, match="Wrong prompt template"):
        KeywordPrompt.compile("Question without a placeholder")
