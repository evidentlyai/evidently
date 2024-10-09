import abc
from abc import ABC
from typing import ClassVar
from typing import List
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.dataset_generators.llm.chunks import Chunk
from evidently.dataset_generators.llm.chunks import IndexExtractor
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.llm import BlockPromptTemplate
from evidently.utils.llm import LLMMessage
from evidently.utils.llm import LLMWrapper
from evidently.utils.llm import PromptBlock
from evidently.utils.llm import PromptTemplate

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]


class QuestionGenerator(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def generate_questions(self, wrapper: LLMWrapper, chunks: Sequence[Chunk]) -> List[GeneratedQuestion]:
        raise NotImplementedError


class SimpleQuestionPrompt(BlockPromptTemplate):
    blocks: ClassVar = [
        PromptBlock.simple("Please generate a {question_type} question about this:"),
        PromptBlock.input("context").anchored(),
        PromptBlock.json_output(question="question text", answer="answer text"),
    ]


class PromptQuestionGenerator(QuestionGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    prompt: PromptTemplate
    question_type: str = "simple"

    def generate_questions(self, wrapper: LLMWrapper, chunks: Sequence[Chunk]) -> GeneratedQuestion:
        context = "\n\n".join(chunks)
        rendered = self.prompt.render(context=context, question_type=self.question_type)
        result = wrapper.complete([LLMMessage.user(rendered)])
        data = self.prompt.parse(result, keys=["question", "answer"])
        return data["question"], data["answer"], context


class QuestionPairGenerator(BaseLLMDatasetGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    index: IndexExtractor
    questions: QuestionGenerator
    num_questions: int

    def generate(self) -> DatasetGeneratorResult:
        documents = self.index.extract_index()
        qs = self.questions.generate_questions(self.wrapper, [chunk for chunk in documents.chunks])

        return pd.DataFrame([qs], columns=["question", "answer", "context"])
