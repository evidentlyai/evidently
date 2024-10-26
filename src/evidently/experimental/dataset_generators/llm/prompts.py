from typing import ClassVar
from typing import List

from evidently.utils.llm.prompts import BlockPromptTemplate
from evidently.utils.llm.prompts import PromptBlock
from evidently.utils.llm.prompts import WithSystemPrompt
from evidently.utils.llm.prompts import llm_call


class SimpleQuestionPromptTemplate(BlockPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:SimpleQuestionPromptTemplate"

    blocks: ClassVar = [
        "Please generate a {question_type} question about this:",
        PromptBlock.input("context").anchored(),
        PromptBlock.json_output(question="question text", answer="answer text"),
    ]
    question_type: str = "simple"


class QuestionsFromSeedPromptTemplate(BlockPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:QuestionsFromSeedPromptTemplate"

    blocks: ClassVar = [
        """Write for me {number} alternative questions quite similar to the question you got.
        The question: """,
        PromptBlock.input("seed_question").anchored(),
        PromptBlock.string_list_output("questions"),
    ]

    @llm_call
    def generate(self, seed_question: str, number: int) -> List[str]: ...  # type: ignore[empty-body]


class QuestionsFromContextPromptTemplate(WithSystemPrompt, BlockPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:QuestionsFromContextPromptTemplate"

    system_prompt: str = "You are an assistant who generates questions based on provided context"

    @llm_call
    def generate_questions(self, context: str, number: int) -> List[str]: ...  # type: ignore[empty-body]


class NaiveQuestionsFromContextPromptTemplate(QuestionsFromContextPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:NaiveQuestionsFromContextPromptTemplate"

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


class ReformulateQuestionPromptTemplate(QuestionsFromContextPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:ReformulateQuestionPromptTemplate"

    blocks: ClassVar = [
        """Write for me {number} alternative questions quite similar to the question you got.
The question:""",
        PromptBlock.input("context").anchored(),
        PromptBlock.string_list_output("questions"),
    ]
    number: int
    system_prompt: str = "You are a smart assistant who helps repharase questions"


class BaselineAnswerPromptTemplate(WithSystemPrompt, BlockPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:BaselineAnswerPromptTemplate"

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
    system_prompt: str = "You are a helpful assistant that answer a given question directly without any preamble"

    @llm_call
    def generate_answers(self, question: str, context: str): ...
