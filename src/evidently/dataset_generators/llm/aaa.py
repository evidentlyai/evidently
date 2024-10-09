import abc
import json
from abc import ABC
from typing import ClassVar
from typing import Iterator
from typing import List
from typing import Tuple

import pandas as pd
from llama_index.core.node_parser import SentenceSplitter

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.llm import LLMMessage
from evidently.utils.llm import LLMWrapper

LLMChunk = str


class ChunkGenerator(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def generate_chunks(self) -> Iterator[LLMChunk]:
        raise NotImplementedError


class FileContextGenerator(ChunkGenerator):
    class Config:
        type_alias = "asdfasdfasd"

    path: str

    def generate_chunks(self) -> Iterator[LLMChunk]:
        with open(self.path) as f:
            text = f.read()
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        text_nodes = splitter.split_text(text)
        yield from text_nodes


class SimpleChunkGenerator(ChunkGenerator):
    class Config:
        type_alias = "asdfasdasdfafasd"

    chunks: List[LLMChunk]

    def generate_chunks(self) -> Iterator[LLMChunk]:
        yield from self.chunks


Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, LLMChunk]


class QuestionGenerator(EvidentlyBaseModel, ABC):
    @abc.abstractmethod
    def generate_question(self, wrapper: LLMWrapper, chunk: LLMChunk) -> GeneratedQuestion:
        raise NotImplementedError


class QuestionPrompt(EvidentlyBaseModel):
    class Config:
        type_alias = "asdfasdasdfaadsfasfasd"

    template: ClassVar[str] = ""


class SimpleQuestionPrompt(QuestionPrompt):
    class Config:
        type_alias = "asdfasdasdfaaasdfadsfasfasd"

    template: ClassVar[str] = (
        'please generate a json with two fields "question" and "answer" with '
        "question and answer about this: {chunk}. dont use markdown in resposne"
    )


class PromptQuestionGenerator(QuestionGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    prompt: QuestionPrompt

    def generate_question(self, wrapper: LLMWrapper, chunk: LLMChunk) -> GeneratedQuestion:
        rendered = self.prompt.template.format(chunk=chunk)

        result = wrapper.complete([LLMMessage.user(rendered)])
        print(result)
        data = json.loads(result)
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
