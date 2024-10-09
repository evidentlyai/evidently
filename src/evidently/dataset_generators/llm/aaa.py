from typing import List
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.dataset_generators.llm.index import Chunk
from evidently.dataset_generators.llm.index import IndexExtractor
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt
from evidently.dataset_generators.llm.prompts import QuestionGenerationPrompt
from evidently.utils.llm import LLMMessage

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]


class QuestionPairGenerator(BaseLLMDatasetGenerator):
    class Config:
        type_alias = "asdfasdasdfaaasdfdsfasfasd"

    index: IndexExtractor
    num_questions: int
    prompt: QuestionGenerationPrompt
    system_prompt: str = "You are an assisstant who generates questions based on provided context"
    answer_prompt: BaselineAnswerPrompt
    answer_system_prompt: str = "You are a helpful assistant thet answer a given question directly without any preamble"

    def generate(self) -> DatasetGeneratorResult:
        documents = self.index.extract_index()
        questions: List[Question] = self.generate_questions([chunk for chunk in documents.chunks])
        relevant_chunks = [[c] for c in documents.chunks]  # fixme
        answers = self.generate_answers(questions, relevant_chunks)
        return pd.DataFrame({"questions": questions, "answers": answers, "context": relevant_chunks})

    def generate_questions(self, chunks: Sequence[Chunk]) -> List[Question]:
        context = "\n\n".join(chunks)
        rendered = self.prompt.render(context=context)
        result = self.wrapper.complete([LLMMessage.system(self.system_prompt), LLMMessage.user(rendered)])
        data = self.prompt.parse(result, keys=["questions"])
        return data["questions"]

    def generate_answers(self, questions: List[Question], relevent_chunks: List[List[Chunk]]):
        answers = []
        system = LLMMessage.system(self.answer_system_prompt)
        for question, chunks in zip(questions, relevent_chunks):
            answer = self.wrapper.complete(
                [system, LLMMessage.user(self.answer_prompt.render(question=question, context="\n".join(chunks)))]
            )
            answers.append(answer)
        return answers
