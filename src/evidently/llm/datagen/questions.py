import random
from math import ceil
from typing import List
from typing import Sequence
from typing import Set
from typing import Tuple

import pandas as pd

from evidently.legacy.utils.llm.prompts import WithSystemPrompt
from evidently.llm.datagen.base import BaseLLMDatasetGenerator
from evidently.llm.datagen.base import DatasetGeneratorResult
from evidently.llm.rag.index import DataCollection
from evidently.llm.rag.index import DataCollectionProvider
from evidently.llm.rag.splitter import Chunk
from evidently.llm.rag.splitter import ChunkSet
from evidently.llm.utils.prompts import StrPromptTemplate
from evidently.llm.utils.prompts import prompt_contract

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]


class QuestionsFromContextPromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are an assistant who generates questions based on provided context"

    @prompt_contract
    def generate_questions(self, context: str, number: int) -> List[str]:
        """Generate {number} conceptual questions based on the provided context and
        can be answered from the information in the provided context.

         {% datagen_instruction(number) %}

        Here is a context
        {% input(context,anchors=True) %}

        {% output_string_list(questions) %}"""
        return []


class BaselineAnswerPromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are a helpful assistant that answer a given question directly without any preamble"

    @prompt_contract
    def generate_answers(self, question: str, context: str):
        """Your task is to answer the following query:
        {% input(question,anchors=True) %}
        You have access to the following documents which are meant to provide context as you answer the query:
        {% input(context,anchors=True) %}
        Please remain faithful to the underlying context,
        and deviate from it only if you haven't found the answer in the provided context.
        Avoid providing any preamble!
        Avoid providing any closing statement!,
        {% output_string(answer) %}"""


class QADatasetGenerator(BaseLLMDatasetGenerator):
    data_collection: DataCollectionProvider
    num_questions: int
    dataset_name: str
    prompt: QuestionsFromContextPromptTemplate = QuestionsFromContextPromptTemplate()
    answers: BaselineAnswerPromptTemplate = BaselineAnswerPromptTemplate()
    include_context: bool

    async def agenerate(self) -> DatasetGeneratorResult:
        documents = self.data_collection.get_data_collection()
        chunk_set_count, chunks_in_set_count, questions_per_chunkset = self.get_chunks_and_question_count(
            len(documents.chunks)
        )
        chunk_sets = self.generate_chunksets(documents, chunk_set_count, chunks_in_set_count)
        questions: List[Question] = await self.agenerate_questions(chunk_sets, questions_per_chunkset)
        relevant_chunks = [documents.find_relevant_chunks(q) for q in questions]
        answers = await self.agenerate_answers(questions, relevant_chunks)
        data = {"questions": questions, "answers": answers}
        if self.include_context:
            data["context"] = [";".join(chunks) for chunks in relevant_chunks]
        return self.dataset_name, pd.DataFrame(data)

    def get_chunks_and_question_count(self, all_chunks_count: int) -> Tuple[int, int, int]:
        questions_per_chunkset = min(10, self.num_questions)
        chunk_set_count = ceil(self.num_questions / questions_per_chunkset)
        chunks_in_set_count = min(5, all_chunks_count)
        return chunk_set_count, chunks_in_set_count, questions_per_chunkset

    def generate_chunksets(self, documents: DataCollection, count: int, chunks_per_set: int) -> List[ChunkSet]:
        return [[random.choice(documents.chunks) for _ in range(chunks_per_set)] for _ in range(count)]

    async def agenerate_questions(
        self, chunk_sets: Sequence[List[Chunk]], questions_per_chunkset: int
    ) -> List[Question]:
        questions = await self.wrapper.run_batch(
            self.prompt.generate_questions(context="\n\n".join(chunks), number=questions_per_chunkset)
            for chunks in chunk_sets
        )
        return [q for qs in questions for q in qs][: self.num_questions]

    async def agenerate_answers(self, questions: List[Question], relevant_chunks: List[List[Chunk]]) -> List[str]:
        return await self.wrapper.run_batch(
            self.answers.generate_answers(question=question, context="\n".join(chunks))
            for question, chunks in zip(questions, relevant_chunks)
        )


class QuestionsFromSeedPromptTemplate(StrPromptTemplate):
    @prompt_contract
    def generate(self, seed_question: str, number: int, context_description: str = "") -> List[str]:
        """
        Generate for me {number} diverse questions like the question you got with respect to the case if provided.

         {% datagen_instruction(number) %}

        Here is a case I'm working on:
        {% input(context_description,anchors=True) %}

        The question:
        {% input(seed_question,anchors=True) %}

        {% output_string_list(questions) %}"""
        return []


class QADatasetFromSeedGenerator(BaseLLMDatasetGenerator):
    seed_question: str
    context_description: str = ""
    num_questions: int
    dataset_name: str
    prompt: QuestionsFromSeedPromptTemplate = QuestionsFromSeedPromptTemplate()

    async def agenerate(self) -> DatasetGeneratorResult:
        max_attempt_count = 3
        attempt_count = 0
        questions_set: Set[str] = set()
        num_questions = self.num_questions
        seed_question = self.seed_question
        while len(questions_set) < self.num_questions and attempt_count < max_attempt_count:
            attempt_count += 1
            num_questions = (num_questions - len(questions_set)) * (attempt_count)
            if len(questions_set) > 0:
                seed_question = random.choice(list(questions_set))
            response = await self.wrapper.run(
                self.prompt.generate(
                    number=num_questions,
                    seed_question=seed_question,
                    context_description=self.context_description,
                )
            )
            questions_set = questions_set | set(response)

        df = pd.DataFrame({"questions": list(questions_set)[: self.num_questions]})
        return self.dataset_name, df
