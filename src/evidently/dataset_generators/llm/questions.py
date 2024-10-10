import random
from typing import List
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.dataset_generators.base import DatasetGeneratorResult
from evidently.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.dataset_generators.llm.index import Chunk
from evidently.dataset_generators.llm.index import DataCollection
from evidently.dataset_generators.llm.index import DataCollectionProvider
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt
from evidently.dataset_generators.llm.prompts import NaiveQuestionsFromContext
from evidently.dataset_generators.llm.prompts import QuestionsFromContext
from evidently.dataset_generators.llm.prompts import QuestionsFromSeed
from evidently.utils.llm import LLMMessage

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]
ChunkSet = List[Chunk]


class QADatasetGenerator(BaseLLMDatasetGenerator):
    data_collection: DataCollectionProvider
    num_questions: int
    questions: QuestionsFromContext = NaiveQuestionsFromContext()
    questions_system_prompt: str = "You are an assistant who generates questions based on provided context"
    answers: BaselineAnswerPrompt = BaselineAnswerPrompt()
    answer_system_prompt: str = "You are a helpful assistant that answer a given question directly without any preamble"

    def generate(self) -> DatasetGeneratorResult:
        documents = self.data_collection.get_data_collection()
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

    def generate_answers(self, questions: List[Question], relevant_chunks: List[List[Chunk]]) -> List[str]:
        system = LLMMessage.system(self.answer_system_prompt)
        return self.wrapper.batch_complete_sync(
            [
                [system, LLMMessage.user(self.answers.render(question=question, context="\n".join(chunks)))]
                for question, chunks in zip(questions, relevant_chunks)
            ]
        )


class QADatasetFromSeedGenerator(BaseLLMDatasetGenerator):
    seed_question: str
    num_questions: int
    prompt: QuestionsFromSeed = QuestionsFromSeed()
    system_prompt: str = "You are a smart assistant who helps repharase questions"

    def generate(self) -> DatasetGeneratorResult:
        response = self.wrapper.batch_complete_sync(
            [
                [
                    LLMMessage.system(self.system_prompt),
                    LLMMessage.user(self.prompt.render(number=self.num_questions, seed_question=self.seed_question)),
                ]
            ]
        )
        return pd.DataFrame({"questions": self.prompt.parse(response[0], keys=["questions"])["questions"]})
