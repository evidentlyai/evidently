import random
from abc import ABC
from math import ceil
from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pandas as pd

from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.llm.datagen.base import BaseLLMDatasetGenerator
from evidently.llm.datagen.base import DatasetGeneratorResult
from evidently.llm.datagen.config import GenerationSpec
from evidently.llm.datagen.config import ServiceSpec
from evidently.llm.datagen.config import UserProfile
from evidently.llm.rag.index import DataCollection
from evidently.llm.rag.index import DataCollectionProvider
from evidently.llm.rag.splitter import Chunk
from evidently.llm.rag.splitter import ChunkSet
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.prompt_render import PreparedTemplate
from evidently.llm.utils.templates import StrPromptTemplate
from evidently.llm.utils.templates import WithSystemPrompt
from evidently.llm.utils.templates import prompt_contract

RAGQuery = str
RAGResponse = str
RAGGeneration = Tuple[RAGQuery, RAGResponse, Chunk]


class RagQueryPromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are an assistant who generates questions based on provided context"

    query_spec: ClassVar[GenerationSpec]
    additional_prompt_blocks: ClassVar[List[PromptBlock]]

    @prompt_contract
    def generate(self, context: str, number: int) -> List[str]:
        """
        {query_spec}

        {additional_prompt_blocks}

        Here is a context
        {% input(context,tag=True) %}

        {% datagen_instruction('{number}') %}

        {% output_string_list(query_spec.kind, tagged=True) %}
        """
        return []


class RagResponsePromptTemplate(WithSystemPrompt, StrPromptTemplate):
    system_prompt: str = "You are a helpful assistant that answer a given question directly without any preamble"

    query_spec: ClassVar[GenerationSpec]
    response_spec: ClassVar[GenerationSpec]
    additional_prompt_blocks: ClassVar[List[PromptBlock]]

    @prompt_contract
    def generate(self, input_value: str, context: str):
        """
        {response_spec}
        {additional_prompt_blocks}

        Your task is to generate {response_spec.kind} to the following {query_spec.kind}:

        {% input(input_value, tag=True) %}

        You have access to the following documents which are meant to provide context as you answer the query:

        {% input(context,tag=True) %}

        Please remain faithful to the underlying context,
        and deviate from it only if you haven't found the answer in the provided context.
        Avoid providing any preamble!
        Avoid providing any closing statement!,

        {% output_string(response_spec.kind) %}
        """


def generate_chunksets(documents: DataCollection, count: int, chunks_per_set: int) -> List[ChunkSet]:
    return [[random.choice(documents.chunks) for _ in range(chunks_per_set)] for _ in range(count)]


class BaseRagDatasetGenerator(BaseLLMDatasetGenerator, ABC):
    data_collection: DataCollectionProvider


class RagQueryDatasetGenerator(BaseRagDatasetGenerator):
    """Dataset generator for RAG queries based on document chunks.

    Generates questions/queries that are relevant to provided document chunks,
    useful for creating evaluation datasets for RAG systems.
    """

    query_template: RagQueryPromptTemplate = RagQueryPromptTemplate()
    """Prompt template for generating queries."""
    query_spec: GenerationSpec = GenerationSpec(kind="question")
    """Specification for query generation."""
    additional_prompt_blocks: List[PromptBlock] = []
    """Additional prompt blocks to include."""
    count: int = 10
    """Number of queries to generate."""
    chunks_per_query: int = 5
    """Number of document chunks to use per query."""

    def __init__(
        self,
        data_collection: DataCollectionProvider,
        count: int = 10,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        complexity: Optional[str] = None,
        query_spec: GenerationSpec = GenerationSpec(kind="question"),
        user: Union[str, UserProfile, None] = None,
        service: Union[str, ServiceSpec, None] = None,
        chunks_per_query: int = 5,
        additional_prompt_blocks: Optional[List[PromptBlock]] = None,
        query_template: Union[str, RagQueryPromptTemplate, None] = None,
        **data: Any,
    ):
        self.data_collection = data_collection
        self.count = count
        self.chunks_per_query = chunks_per_query
        additional: List[PromptBlock] = additional_prompt_blocks or []
        if user is not None:
            additional.append(user if isinstance(user, UserProfile) else UserProfile(role=user))
        if service is not None:
            additional.append(
                service if isinstance(service, ServiceSpec) else ServiceSpec(kind="RAG", description=service)
            )
        self.additional_prompt_blocks = additional

        if query_spec is not None:
            self.query_spec = query_spec
        else:
            self.query_spec = GenerationSpec(kind="question", complexity=complexity or "medium")

        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        if isinstance(query_template, str):
            self.query_template = RagQueryPromptTemplate(prompt_template=query_template)
        else:
            self.query_template = query_template or RagQueryPromptTemplate()
        super().__init__(**data)

    def get_chunks_and_query_count(self, all_chunks_count: int) -> Tuple[int, int, int]:
        """Calculate chunk and query counts for generation.

        Args:
        * `all_chunks_count`: Total number of available chunks.

        Returns:
        * Tuple of (chunk_set_count, chunks_in_set_count, questions_per_chunkset).
        """
        questions_per_chunkset = min(10, self.count)
        chunk_set_count = ceil(self.count / questions_per_chunkset)
        chunks_in_set_count = min(self.chunks_per_query, all_chunks_count)
        return chunk_set_count, chunks_in_set_count, questions_per_chunkset

    async def generate_queries_with_context(self) -> Tuple[DataCollection, List[RAGQuery]]:
        """Generate queries along with their document context.

        Returns:
        * Tuple of (data_collection, list of generated queries).
        """
        documents = self.data_collection.get_data_collection()
        chunk_set_count, chunks_in_set_count, questions_per_chunkset = self.get_chunks_and_query_count(
            len(documents.chunks)
        )
        chunk_sets = generate_chunksets(documents, chunk_set_count, chunks_in_set_count)
        queries: List[RAGQuery] = await self.generate_queries(chunk_sets, questions_per_chunkset)
        return documents, queries

    async def agenerate(self) -> DatasetGeneratorResult:
        """Generate dataset asynchronously.

        Returns:
        * `pd.DataFrame` with generated queries in a "queries" column.
        """
        _, queries = await self.generate_queries_with_context()
        return pd.DataFrame({"queries": queries})

    async def generate_queries(self, chunk_sets: Sequence[List[Chunk]], questions_per_chunkset: int) -> List[RAGQuery]:
        """Generate queries from chunk sets.

        Args:
        * `chunk_sets`: Sequence of chunk lists to generate queries from.
        * `questions_per_chunkset`: Number of questions to generate per chunk set.

        Returns:
        * List of generated query strings.
        """
        with self.query_template.with_context(
            query_spec=self.query_spec, additional_prompt_blocks=self.additional_prompt_blocks
        ):
            requests = [
                self.query_template.generate(context="\n\n".join(chunks), number=questions_per_chunkset)
                for chunks in chunk_sets
            ]
        questions = await self.wrapper.run_batch(requests)
        return [q for qs in questions for q in qs][: self.count]

    @property
    def prepared_query_template(self) -> PreparedTemplate:
        """Get the prepared query template with all context applied.

        Returns:
        * `PreparedTemplate` ready for use with the LLM.
        """
        return self.query_template.prepare(
            query_spec=self.query_spec, additional_prompt_blocks=self.additional_prompt_blocks
        )


class RagResponseDatasetGenerator(BaseRagDatasetGenerator):
    """Dataset generator for RAG responses based on queries and document chunks.

    Generates responses to queries using relevant document chunks as context,
    useful for creating evaluation datasets for RAG systems.
    """

    response_template: RagResponsePromptTemplate = RagResponsePromptTemplate()
    """Prompt template for generating responses."""
    response_spec: GenerationSpec = GenerationSpec(kind="response")
    """Specification for response generation."""
    query_spec: GenerationSpec = GenerationSpec(kind="question")
    """Specification for query type."""
    queries: List[RAGQuery]
    """List of queries to generate responses for."""
    additional_prompt_blocks: List[PromptBlock] = []
    """Additional prompt blocks to include."""
    include_context: bool = False
    """Whether to include context chunks in output DataFrame."""

    def __init__(
        self,
        data_collection: DataCollectionProvider,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        include_context: bool = False,
        complexity: Optional[str] = None,
        query_spec: GenerationSpec = GenerationSpec(kind="question"),
        response_spec: GenerationSpec = GenerationSpec(kind="answer"),
        user: Union[str, UserProfile, None] = None,
        service: Union[str, ServiceSpec, None] = None,
        additional_prompt_blocks: Optional[List[PromptBlock]] = None,
        response_template: Union[str, RagResponsePromptTemplate, None] = None,
        **data: Any,
    ):
        self.data_collection = data_collection
        self.include_context = include_context
        additional: List[PromptBlock] = additional_prompt_blocks or []
        if user is not None:
            additional.append(user if isinstance(user, UserProfile) else UserProfile(role=user))
        if service is not None:
            additional.append(
                service if isinstance(service, ServiceSpec) else ServiceSpec(kind="RAG", description=service)
            )
        self.additional_prompt_blocks = additional

        if query_spec is not None:
            self.query_spec = query_spec
        else:
            self.query_spec = GenerationSpec(kind="question", complexity=complexity or "medium")

        if response_spec is not None:
            self.response_spec = response_spec
        else:
            self.response_spec = GenerationSpec(kind="answer", complexity=complexity or "medium")

        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        if isinstance(response_template, str):
            self.response_template = RagResponsePromptTemplate(prompt_template=response_template)
        else:
            self.response_template = response_template or RagResponsePromptTemplate()
        super().__init__(**data)

    async def agenerate(self) -> DatasetGeneratorResult:
        """Generate dataset asynchronously.

        Returns:
        * `pd.DataFrame` with generated responses (and optionally context).
        """
        documents = self.data_collection.get_data_collection()
        relevant_chunks = [documents.find_relevant_chunks(q) for q in self.queries]
        responses = await self.generate_responses(self.queries, relevant_chunks)
        data = {"responses": responses}
        if self.include_context:
            data["context"] = [";".join(chunks) for chunks in relevant_chunks]
        return pd.DataFrame(data)

    async def generate_responses(self, queries: List[RAGQuery], relevant_chunks: List[List[Chunk]]) -> List[str]:
        """Generate responses for queries using relevant chunks as context.

        Args:
        * `queries`: List of query strings.
        * `relevant_chunks`: List of chunk lists, one per query.

        Returns:
        * List of generated response strings.
        """
        with self.response_template.with_context(
            response_spec=self.response_spec,
            query_spec=self.query_spec,
            additional_prompt_blocks=self.additional_prompt_blocks,
        ):
            requests = [
                self.response_template.generate(input_value=question, context="\n".join(chunks))
                for question, chunks in zip(queries, relevant_chunks)
            ]
        return await self.wrapper.run_batch(requests)

    @property
    def prepared_response_template(self) -> PreparedTemplate:
        """Get the prepared response template with all context applied.

        Returns:
        * `PreparedTemplate` ready for use with the LLM.
        """
        return self.response_template.prepare(
            query_spec=self.query_spec,
            additional_prompt_blocks=self.additional_prompt_blocks,
            response_spec=self.response_spec,
        )


class RagDatasetGenerator(BaseRagDatasetGenerator):
    """Complete RAG dataset generator for query-response pairs.

    Generates both queries and responses using document chunks, creating
    a complete evaluation dataset for RAG systems.
    """

    query_template: RagQueryPromptTemplate = RagQueryPromptTemplate()
    """Prompt template for generating queries."""
    query_spec: GenerationSpec = GenerationSpec(kind="question")
    """Specification for query generation."""
    response_spec: GenerationSpec = GenerationSpec(kind="response")
    """Specification for response generation."""
    response_template: RagResponsePromptTemplate = RagResponsePromptTemplate()
    """Prompt template for generating responses."""
    additional_prompt_blocks: List[PromptBlock] = []
    """Additional prompt blocks to include."""
    include_context: bool = False
    """Whether to include context chunks in output DataFrame."""
    count: int
    """Number of query-response pairs to generate."""

    def __init__(
        self,
        data_collection: DataCollectionProvider,
        count: int = 10,
        model="gpt-4o-mini",
        provider="openai",
        options: AnyOptions = None,
        include_context: bool = False,
        complexity: Optional[str] = None,
        query_spec: GenerationSpec = GenerationSpec(kind="question"),
        response_spec: GenerationSpec = GenerationSpec(kind="response"),
        user: Union[str, UserProfile, None] = None,
        service: Union[str, ServiceSpec, None] = None,
        additional_prompt_blocks: Optional[List[PromptBlock]] = None,
        query_template: Union[str, RagQueryPromptTemplate, None] = None,
        response_template: Union[str, RagResponsePromptTemplate, None] = None,
        **data: Any,
    ):
        self.data_collection = data_collection
        self.include_context = include_context
        self.count = count
        additional: List[PromptBlock] = additional_prompt_blocks or []
        if user is not None:
            additional.append(user if isinstance(user, UserProfile) else UserProfile(role=user))
        if service is not None:
            additional.append(service if isinstance(service, ServiceSpec) else ServiceSpec(kind="RAG", purpose=service))
        self.additional_prompt_blocks = additional

        if query_spec is not None:
            self.query_spec = query_spec
        else:
            self.query_spec = GenerationSpec(kind="question", complexity=complexity or "medium")

        if response_spec is not None:
            self.response_spec = response_spec
        else:
            self.response_spec = GenerationSpec(kind="answer", complexity=complexity or "medium")

        self.provider = provider
        self.options = Options.from_any_options(options)
        self.model = model
        if isinstance(query_template, str):
            self.query_template = RagQueryPromptTemplate(prompt_template=query_template)
        else:
            self.query_template = query_template or RagQueryPromptTemplate()
        if isinstance(response_template, str):
            self.response_template = RagResponsePromptTemplate(prompt_template=response_template)
        else:
            self.response_template = response_template or RagResponsePromptTemplate()
        super().__init__(**data)

    async def agenerate(self) -> DatasetGeneratorResult:
        """Generate complete RAG dataset with queries and responses.

        Returns:
        * `pd.DataFrame` with "queries" and "responses" columns (and optionally "context").
        """
        documents, queries = await self.query_generator.generate_queries_with_context()
        relevant_chunks = [documents.find_relevant_chunks(q) for q in queries]

        response_generator = self.response_generator(queries)
        responses = await response_generator.generate_responses(queries, relevant_chunks)
        data = {"queries": queries, "responses": responses}
        if self.include_context:
            data["context"] = [";".join(chunks) for chunks in relevant_chunks]
        return pd.DataFrame(data)

    @property
    def query_generator(self) -> RagQueryDatasetGenerator:
        """Get the query generator instance.

        Returns:
        * `RagQueryDatasetGenerator` configured with this generator's settings.
        """
        return RagQueryDatasetGenerator(
            data_collection=self.data_collection,
            count=self.count,
            query_spec=self.query_spec,
            query_template=self.query_template,
            additional_prompt_blocks=self.additional_prompt_blocks,
            options=self.options,
            provider=self.provider,
            model=self.model,
        )

    def response_generator(self, queries: List[RAGQuery]) -> RagResponseDatasetGenerator:
        """Get the response generator instance for given queries.

        Args:
        * `queries`: List of queries to generate responses for.

        Returns:
        * `RagResponseDatasetGenerator` configured with this generator's settings.
        """
        return RagResponseDatasetGenerator(
            data_collection=self.data_collection,
            query_spec=self.query_spec,
            response_spec=self.response_spec,
            response_template=self.response_template,
            additional_prompt_blocks=self.additional_prompt_blocks,
            queries=queries,
            options=self.options,
            provider=self.provider,
            model=self.model,
        )

    @property
    def prepared_query_template(self) -> PreparedTemplate:
        """Get the prepared query template.

        Returns:
        * `PreparedTemplate` ready for use with the LLM.
        """
        return self.query_generator.prepared_query_template

    @property
    def prepared_response_template(self) -> PreparedTemplate:
        """Get the prepared response template.

        Returns:
        * `PreparedTemplate` ready for use with the LLM.
        """
        return self.response_generator([]).prepared_response_template
