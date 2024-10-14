import random
from typing import List
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.experimental.dataset_generators.base import DatasetGeneratorResult
from evidently.experimental.dataset_generators.llm.base import BaseLLMDatasetGenerator
from evidently.experimental.dataset_generators.llm.index import Chunk
from evidently.experimental.dataset_generators.llm.index import DataCollection
from evidently.experimental.dataset_generators.llm.index import DataCollectionProvider
from evidently.experimental.dataset_generators.llm.prompts import BaselineAnswerPrompt
from evidently.experimental.dataset_generators.llm.prompts import NaiveQuestionsFromContext
from evidently.experimental.dataset_generators.llm.prompts import QuestionsFromContext
from evidently.experimental.dataset_generators.llm.prompts import QuestionsFromSeed

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]
ChunkSet = List[Chunk]


class QADatasetGenerator(BaseLLMDatasetGenerator):
    data_collection: DataCollectionProvider
    num_questions: int
    questions: QuestionsFromContext = NaiveQuestionsFromContext()
    answers: BaselineAnswerPrompt = BaselineAnswerPrompt()

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
        questions = self.wrapper.run_batch_sync(
            self.questions.generate_questions(context="\n\n".join(chunks), number=questions_per_chunkset)
            for chunks in chunk_sets
        )
        return [q for qs in questions for q in qs]

    def generate_answers(self, questions: List[Question], relevant_chunks: List[List[Chunk]]) -> List[str]:
        return self.wrapper.run_batch_sync(
            self.answers.generate_answers(question=question, context="\n".join(chunks))
            for question, chunks in zip(questions, relevant_chunks)
        )


class QADatasetFromSeedGenerator(BaseLLMDatasetGenerator):
    seed_question: str
    num_questions: int
    prompt: QuestionsFromSeed = QuestionsFromSeed()

    def generate(self) -> DatasetGeneratorResult:
        response = self.wrapper.run_sync(
            self.prompt.generate(number=self.num_questions, seed_question=self.seed_question)
        )

        return pd.DataFrame({"questions": response})
