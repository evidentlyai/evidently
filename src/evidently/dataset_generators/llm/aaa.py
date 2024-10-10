import random
from typing import List
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.dataset_generators.llm.index import Chunk
from evidently.dataset_generators.llm.index import DataCollection

# from evidently.dataset_generators.llm.index import IndexExtractor
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt
from evidently.dataset_generators.llm.prompts import QuestionGenerationPrompt
from evidently.utils.llm import LLMMessage

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]
ChunkSet = List[Chunk]


class DatasetFromDocs(BaseLLMDatasetGenerator):
    class Config:
        type_alias = "DatasetFromDocs"
        arbitrary_types_allowed = True

    data_collection: DataCollection
    num_questions: int
    questions: QuestionGenerationPrompt
    questions_system_prompt: str = "You are an assisstant who generates questions based on provided context"
    answers: BaselineAnswerPrompt
    answer_system_prompt: str = "You are a helpful assistant thet answer a given question directly without any preamble"

    def generate(self) -> DatasetGeneratorResult:
        documents = self.data_collection
        chunk_set_count, chunks_in_set_count, questions_per_chunkset = self.get_chunks_and_question_count()
        chunk_sets = self.generate_chunksets(documents, chunk_set_count, chunks_in_set_count)
        questions: List[Question] = self.generate_questions(chunk_sets, questions_per_chunkset)
        relevant_chunks = [documents.find_relevant_chunks(q) for q in questions]
        answers = self.generate_answers(questions, relevant_chunks)
        return pd.DataFrame({"questions": questions, "answers": answers, "context": relevant_chunks})

    def get_chunks_and_question_count(self) -> Tuple[int, int, int]:
        return 1, 1, self.num_questions

    def generate_chunksets(self, documents: DataCollection, count: int, chunks_per_set: int) -> List[ChunkSet]:
        return [[random.choice(documents.chunks) for _ in range(chunks_per_set)] for _ in range(count)]

    def generate_questions(self, chunk_sets: Sequence[List[Chunk]], questions_per_chunkset: int) -> List[Question]:
        system = LLMMessage.system(self.questions_system_prompt)
        llm_responses = self.wrapper.batch_complete_sync(
            [
                [
                    system,
                    LLMMessage.user(self.questions.render(context="\n\n".join(chunks), number=questions_per_chunkset)),
                ]
                for chunks in chunk_sets
            ]
        )
        questions = [self.questions.parse(response, keys=["questions"])["questions"] for response in llm_responses]
        return [q for qs in questions for q in qs]

    def generate_answers(self, questions: List[Question], relevent_chunks: List[List[Chunk]]) -> List[str]:
        system = LLMMessage.system(self.answer_system_prompt)
        return self.wrapper.batch_complete_sync(
            [
                [system, LLMMessage.user(self.answers.render(question=question, context="\n".join(chunks)))]
                for question, chunks in zip(questions, relevent_chunks)
            ]
        )
