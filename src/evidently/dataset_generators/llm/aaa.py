import abc
from abc import ABC
from typing import ClassVar
from typing import List
from typing import Tuple

import pandas as pd

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.dataset_generators.llm.chunks import ChunkGenerator
from evidently.dataset_generators.llm.chunks import LLMChunk
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.llm import BlockPromptTemplate
from evidently.utils.llm import LLMMessage
from evidently.utils.llm import LLMWrapper
from evidently.utils.llm import PromptBlock
from evidently.utils.llm import PromptTemplate

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, LLMChunk]


class QuestionGenerator(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def generate_question(self, wrapper: LLMWrapper, chunk: LLMChunk) -> GeneratedQuestion:
        raise NotImplementedError


class SimpleQuestionPrompt(BlockPromptTemplate):
    blocks: ClassVar = [
        PromptBlock.simple("Please generate a question {} about this:"),
        PromptBlock.input("chunk").anchored(),
        PromptBlock.json_output(question="question text", answer="answer text"),
    ]


class PromptQuestionGenerator(QuestionGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    prompt: PromptTemplate

    def generate_question(self, wrapper: LLMWrapper, chunk: LLMChunk) -> GeneratedQuestion:
        rendered = self.prompt.render(chunk=chunk)
        result = wrapper.complete([LLMMessage.user(rendered)])
        data = self.prompt.parse(result)
        return data["question"], data["answer"], chunk


class QuestionPairGenerator(BaseLLMDatasetGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    chunks: ChunkGenerator
    questions: QuestionGenerator
    num_questions: int

    def generate(self) -> DatasetGeneratorResult:
        qs: List[GeneratedQuestion] = []
        for chunk in self.chunks.generate_chunks():
            for i in range(self.num_questions):
                qs.append(self.questions.generate_question(self.wrapper, chunk))

        return pd.DataFrame(qs, columns=["question", "answer", "context"])
