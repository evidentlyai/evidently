from typing import ClassVar

from evidently.utils.llm import BlockPromptTemplate
from evidently.utils.llm import PromptBlock


class SimpleQuestionPrompt(BlockPromptTemplate):
    blocks: ClassVar = [
        "Please generate a {question_type} question about this:",
        PromptBlock.input("context").anchored(),
        PromptBlock.json_output(question="question text", answer="answer text"),
    ]
    question_type: str = "simple"


class QuestionGenerationPrompt(BlockPromptTemplate):
    pass


class NaiveQuestionsPrompt(QuestionGenerationPrompt):
    blocks: ClassVar = [
        "Generate {number} conceptual questions based on the provided context and "
        "can be answered from the information in the provided context.\n"
        "Here is a context",
        PromptBlock.input("context").anchored(),
        "Remain faithful to the above context.\n"
        "Avoid providing any preamble!\n"
        "Avoid providing any closing statement!",
        PromptBlock.string_list_output("questions"),
    ]
    number: int


class ReformulateQuestionPrompt(QuestionGenerationPrompt):
    blocks: ClassVar = [
        """Write for me {number} alternative questions quite similar to the question you got.
The question:""",
        PromptBlock.input("context").anchored(),
        PromptBlock.string_list_output("questions"),
    ]
    number: int


class BaselineAnswerPrompt(BlockPromptTemplate):
    blocks: ClassVar = [
        "Your task is to answer the following query:",
        PromptBlock.input("question").anchored(),
        "You have access to the following documents which are meant to provide context as you answer the query:",
        PromptBlock.input("context").anchored(),
        """Please remain faithful to the underlying context,
and deviate from it only if you haven't found the answer in the provided context.
Avoid providing any preamble!
Avoid providing any closing statement!""",
        PromptBlock.string_output("answer"),
    ]
