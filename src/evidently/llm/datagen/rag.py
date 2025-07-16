import random
from math import ceil
from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

import pandas as pd

from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.prompts import WithSystemPrompt
from evidently.llm.datagen.base import BaseLLMDatasetGenerator
from evidently.llm.datagen.base import DatasetGeneratorResult
from evidently.llm.rag.index import DataCollection
from evidently.llm.rag.index import DataCollectionProvider
from evidently.llm.rag.splitter import Chunk
from evidently.llm.rag.splitter import ChunkSet
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.blocks import SimpleBlock
from evidently.llm.utils.templates import StrPromptTemplate
from evidently.llm.utils.templates import prompt_command
from evidently.llm.utils.templates import prompt_contract

Question = str
Answer = str
GeneratedQuestion = Tuple[Question, Answer, Chunk]


@prompt_command("datagen_instruction")
def datagen_instruction_block(number):
    instruction = f"""Instructions:
•	Make sure the sentence are not exactly repeats of each other.
•	Remain faithful to the above context.
•	Make sure you do not start sentence with hyphen sign.
•	Make sure you do not end sentence with a newline.
•	Avoid providing any preamble.
•	Avoid providing any closing statement.
•	Ensure the number of generated texts is exactly {number}"""
    return SimpleBlock(value=instruction)


class UserProfile(PromptBlock):
    intent: str = None
    role: Optional[str] = None
    tone: str = "neutral"

    def render(self) -> str:
        messages = ["Assume the user profile is:"]
        if self.intent is not None:
            messages.append(f"- Intent: {self.intent}")
        if self.role is not None:
            messages.append(f"- Role: {self.role}")
        messages.append(f"- Tone: {self.tone}")
        return "\n".join(messages)


class RagService(PromptBlock):
    description: str
    user_profile: Optional[UserProfile] = None

    def render(self):
        messages = [f"The RAG system is built for the following service: {self.description}"]
        if self.user_profile is not None:
            messages.append(self.user_profile.render())
        return "\n".join(messages)


class RagInputs(PromptBlock):
    kind: Optional[str] = "question"
    examples: List[str] = []
    complexity: str = "medium"

    def render(self):
        res = [f"Generate standalone {self.kind}s with {self.complexity} complexity."]

        if self.examples:
            res.append("Use these examples as stylistic guidance:")
            for ex in self.examples:
                res.append(f"- {ex}")
        return "\n".join(res)


class RagOutputs(PromptBlock):
    kind: Optional[str] = "answer"


class RagConfig(PromptBlock):
    inputs: RagInputs = RagInputs()
    outputs: RagOutputs = RagOutputs()
    service: RagService = RagService(description="RAG service")
    count: int = 10
    include_context: bool = False


class RagInputsPromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are an assistant who generates questions based on provided context"
    config: ClassVar[RagConfig]

    @prompt_contract
    def generate(self, context: str, number: int) -> List[str]:
        """{config.inputs}
        {config.service}
        {% datagen_instruction('{number}') %}
        Here is a context
        {% input(context,tag=True) %}
        {% output_string_list(config.inputs.kind) %}"""
        return []


class RagOutputsPromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are a helpful assistant that answer a given question directly without any preamble"

    config: ClassVar[RagConfig]

    @prompt_contract
    def generate(self, input_value: str, context: str):
        """
        {config.service}
        Your task is to generate {config.outputs.kind} to the following {config.inputs.kind}:
        {% input(input_value, tag=True) %}
        You have access to the following documents which are meant to provide context as you answer the query:
        {% input(context,tag=True) %}
        Please remain faithful to the underlying context,
        and deviate from it only if you haven't found the answer in the provided context.
        Avoid providing any preamble!
        Avoid providing any closing statement!,
        {% output_string(config.outputs.kind) %}"""


def generate_chunksets(documents: DataCollection, count: int, chunks_per_set: int) -> List[ChunkSet]:
    return [[random.choice(documents.chunks) for _ in range(chunks_per_set)] for _ in range(count)]


class RagDatasetGenerator(BaseLLMDatasetGenerator):
    dataset_name: str
    data_collection: DataCollectionProvider
    inputs: RagInputsPromptTemplate = RagInputsPromptTemplate()
    outputs: RagOutputsPromptTemplate = RagOutputsPromptTemplate()
    config: RagConfig = RagConfig()

    def __init__(
        self,
        dataset_name: str,
        data_collection: DataCollectionProvider,
        config: Optional[RagConfig] = None,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        inputs: Union[str, RagInputsPromptTemplate, None] = None,
        outputs: Union[str, RagOutputsPromptTemplate, None] = None,
        **data: Any,
    ):
        self.data_collection = data_collection
        self.config = config or RagConfig()
        self.dataset_name = dataset_name
        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        self.inputs = inputs
        if isinstance(inputs, str):
            self.inputs = RagInputsPromptTemplate(prompt_template=inputs)
        else:
            self.inputs = inputs or RagInputsPromptTemplate()
        if isinstance(outputs, str):
            self.outputs = RagOutputsPromptTemplate(prompt_template=outputs)
        else:
            self.outputs = outputs or RagOutputsPromptTemplate()
        super().__init__(**data)

    async def agenerate(self) -> DatasetGeneratorResult:
        documents = self.data_collection.get_data_collection()
        chunk_set_count, chunks_in_set_count, questions_per_chunkset = self.get_chunks_and_question_count(
            len(documents.chunks)
        )
        chunk_sets = generate_chunksets(documents, chunk_set_count, chunks_in_set_count)
        inputs: List[Question] = await self.agenerate_inputs(chunk_sets, questions_per_chunkset)
        relevant_chunks = [documents.find_relevant_chunks(q) for q in inputs]
        outputs = await self.agenerate_outputs(inputs, relevant_chunks)
        data = {"inputs": inputs, "outputs": outputs}
        if self.config.include_context:
            data["context"] = [";".join(chunks) for chunks in relevant_chunks]
        return self.dataset_name, pd.DataFrame(data)

    def get_chunks_and_question_count(self, all_chunks_count: int) -> Tuple[int, int, int]:
        questions_per_chunkset = min(10, self.config.count)
        chunk_set_count = ceil(self.config.count / questions_per_chunkset)
        chunks_in_set_count = min(5, all_chunks_count)
        return chunk_set_count, chunks_in_set_count, questions_per_chunkset

    async def agenerate_inputs(self, chunk_sets: Sequence[List[Chunk]], questions_per_chunkset: int) -> List[Question]:
        with self.inputs.with_context(config=self.config):
            requests = [
                self.inputs.generate(context="\n\n".join(chunks), number=questions_per_chunkset)
                for chunks in chunk_sets
            ]
        questions = await self.wrapper.run_batch(requests)
        return [q for qs in questions for q in qs][: self.config.count]

    async def agenerate_outputs(self, inputs: List[Question], relevant_chunks: List[List[Chunk]]) -> List[str]:
        with self.outputs.with_context(config=self.config):
            requests = [
                self.outputs.generate(input_value=question, context="\n".join(chunks))
                for question, chunks in zip(inputs, relevant_chunks)
            ]
        return await self.wrapper.run_batch(requests)


class SeedConfig(PromptBlock):
    inputs: RagInputs = RagInputs()
    service: RagService = RagService(description="Rag service")
    count: int = 10
    seed: str


class InputSeedPromptTemplate(StrPromptTemplate):
    config: ClassVar[SeedConfig]

    @prompt_contract
    def generate(self, input_seed: str, context_description: str) -> List[str]:
        """
        {config.inputs}
        {config.service}
        {% datagen_instruction(config.count) %}

        Here is a case I'm working on:
        {% input(context_description,tag=True) %}

        The input:
        {% input(input_seed,tag=True) %}

        {% output_string_list(config.inputs.kind) %}"""
        return []


class InputSeedDatasetGenerator(BaseLLMDatasetGenerator):
    dataset_name: str
    inputs: InputSeedPromptTemplate
    config: SeedConfig

    def __init__(
        self,
        dataset_name: str,
        config: Optional[SeedConfig] = None,
        inputs: Union[str, RagInputsPromptTemplate, None] = None,
        seed: Optional[str] = None,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        **data: Any,
    ):
        if config is None:
            if seed is None:
                raise ValueError("Either seed or config must be specified")
            config = SeedConfig(count=10, seed=seed)
        self.config = config
        self.dataset_name = dataset_name
        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        if isinstance(inputs, str):
            self.inputs = InputSeedPromptTemplate(prompt_template=inputs)
        else:
            self.inputs = inputs or InputSeedPromptTemplate()
        super().__init__(**data)

    async def agenerate(self) -> DatasetGeneratorResult:
        max_attempt_count = 3
        attempt_count = 0
        inputs_set: Set[str] = set()
        num_questions = self.config.count
        seed_question = self.config.seed
        while len(inputs_set) < num_questions and attempt_count < max_attempt_count:
            attempt_count += 1
            num_questions = (num_questions - len(inputs_set)) * attempt_count
            if len(inputs_set) > 0:
                seed_question = random.choice(list(inputs_set))
            with self.inputs.with_context(config=self.config):
                requests = self.inputs.generate(
                    input_seed=seed_question,
                    context_description=self.config.service.description,
                )
            response = await self.wrapper.run(requests)
            inputs_set = inputs_set | set(response)

        df = pd.DataFrame({"inputs": list(inputs_set)[:num_questions]})
        return self.dataset_name, df
