import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import numpy as np
import pandas as pd

from evidently.core.datasets import AnyDescriptorTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.legacy.base_metric import DisplayName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import OpenAIWrapper
from evidently.legacy.utils.llm.wrapper import get_llm_wrapper


def semantic_similarity_scoring(question: DatasetColumn, context: DatasetColumn, options: Options) -> DatasetColumn:
    """Compute semantic similarity scores between question and context using sentence transformers."""
    from sentence_transformers import SentenceTransformer

    model_id: str = "all-MiniLM-L6-v2"

    def normalized_cosine_distance(left, right):
        """Calculate normalized cosine distance between two vectors."""
        return 1 - ((1 - np.dot(left, right) / (np.linalg.norm(left) * np.linalg.norm(right))) / 2)

    model = SentenceTransformer(model_id)
    context_column = context.data.name
    no_index_context = context.data.reset_index()

    first = model.encode(question.data.fillna(""))
    context_rows = no_index_context.explode([context_column]).reset_index()
    second = model.encode(context_rows[context_column].fillna(""))

    scores = pd.Series(data=[[x] for x in second], index=context_rows.index)
    scind = pd.DataFrame(data={"ind": context_rows["index"], "scores": scores})
    rsd = pd.Series([scind.iloc[x]["scores"] for x in scind.groupby("ind").groups.values()])
    return DatasetColumn(
        data=pd.Series(
            [[normalized_cosine_distance(x, y1[0]) for y1 in y] for x, y in zip(first, rsd)],
            index=question.data.index,
        ),
        type=ColumnType.List,
    )


def llm_scoring(
    question: DatasetColumn,
    context: DatasetColumn,
    options: Options,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
) -> DatasetColumn:
    """Compute relevance scores between question and context using LLM."""
    # unwrap data to rows
    context_column = context.data.name
    no_index_context = context.data.reset_index()
    context_rows = no_index_context.explode([context_column]).reset_index()  #

    llm_wrapper: Optional[LLMWrapper]
    # do scoring
    if provider == "openai":
        llm_wrapper = OpenAIWrapper(model, options)
    else:
        llm_wrapper = get_llm_wrapper(provider, model, options)
    if llm_wrapper is None:
        raise ValueError(f"LLM Wrapper for found for {provider}")
    template = BinaryClassificationPromptTemplate(
        criteria="""A “RELEVANT” label means that the CONTEXT provides useful, supportive, or related information to the QUESTION.

        An “IRRELEVANT” label means that the CONTEXT is either contradictory or unrelated to the QUESTION.

                Here is a QUESTION
                -----question_starts-----
                {input}
                -----question_ends-----

                Here is a CONTEXT
                -----context_starts-----
                {context}
                -----context_ends-----

        """,
        target_category="RELEVANT",
        non_target_category="IRRELEVANT",
        uncertainty="unknown",
        include_reasoning=True,
        include_score=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
    )
    df = pd.DataFrame({"input": question.data, "context": context.data}).explode("context").reset_index()
    questions = template.iterate_messages(df, {"input": "input", "context": "context"})
    results = llm_wrapper.run_batch_sync(questions)
    result_data = pd.DataFrame(results)
    # wrap scoring to lists back
    scind = pd.DataFrame(data={"ind": context_rows["index"], "scores": result_data["score"]})
    rsd = pd.Series(
        [list(scind.iloc[x]["scores"].astype(float)) for x in scind.groupby("ind").groups.values()],
        index=question.data.index,
    )

    return DatasetColumn(
        ColumnType.List,
        rsd,
    )


T = TypeVar("T")


class AggregationMethod(Generic[T]):
    """Base class for aggregating relevance scores."""

    column_type: ColumnType

    @abc.abstractmethod
    def do(self, scores: List[float]) -> T:
        """Aggregate a list of scores into a single value."""
        raise NotImplementedError


class MeanAggregation(AggregationMethod[float]):
    """Aggregate scores by computing the mean."""

    column_type: ColumnType
    """Output column type (Numerical)."""

    def __init__(self):
        self.column_type = ColumnType.Numerical

    def do(self, scores: List[float]) -> float:
        """Return the average of scores."""
        return float(np.average(scores))


class HitAggregation(AggregationMethod[int]):
    """Aggregate scores by checking if any score exceeds threshold."""

    column_type: ColumnType
    """Output column type (Categorical)."""
    threshold: float
    """Score threshold for hit detection."""

    def __init__(self, threshold: float = 0.8):
        self.column_type = ColumnType.Categorical
        self.threshold = threshold

    def do(self, scores: List[float]) -> int:
        """Return 1 if any score >= threshold, else 0."""
        return 1 if any([x >= self.threshold for x in scores]) else 0


class HitShareAggregation(AggregationMethod[float]):
    """Aggregate scores by computing the share of scores above threshold."""

    column_type: ColumnType
    """Output column type (Categorical)."""
    threshold: float
    """Score threshold for hit detection."""

    def __init__(self, threshold: float = 0.8):
        self.column_type = ColumnType.Categorical
        self.threshold = threshold

    def do(self, scores: List[float]) -> float:
        """Return the fraction of scores >= threshold."""
        return float(sum([1 if x >= self.threshold else 0 for x in scores])) / len(scores)


class ScoringMethod(Protocol):
    """Protocol for scoring methods that compute relevance between question and context."""

    def __call__(
        self,
        question: DatasetColumn,
        context: DatasetColumn,
        options: Options,
    ) -> DatasetColumn: ...


METHODS: Dict[str, Tuple[ScoringMethod, Type[MeanAggregation]]] = {
    "semantic_similarity": (semantic_similarity_scoring, MeanAggregation),
    "llm": (llm_scoring, MeanAggregation),
}


AGGREGATION_METHODS = {
    "mean": MeanAggregation,
    "hit": HitAggregation,
    "hit_share": HitShareAggregation,
}


class ContextRelevance(Descriptor):
    """Evaluate relevance of context to input using semantic similarity or LLM scoring."""

    input: str
    """Column name containing input/question text."""
    contexts: str
    """Column name containing context text (list of strings per row)."""
    method: str = "semantic_similarity"
    """Scoring method: "semantic_similarity" or "llm"."""
    method_params: Optional[Dict[str, object]] = None
    """Additional parameters for scoring method."""
    aggregation_method: Optional[str] = None
    """How to aggregate scores: "mean", "hit", or "hit_share"."""
    aggregation_method_params: Optional[Dict[str, object]] = None
    """Parameters for aggregation method."""
    output_scores: bool = False
    """Whether to output individual scores in addition to aggregated score."""

    def __init__(
        self,
        input: str,
        contexts: str,
        method: str = "semantic_similarity",
        method_params: Optional[Dict[str, object]] = None,
        aggregation_method: Optional[str] = None,
        aggregation_method_params: Optional[Dict[str, object]] = None,
        output_scores: bool = False,
        alias: Optional[str] = None,
        tests: Optional[List[AnyDescriptorTest]] = None,
    ):
        self.output_scores = output_scores
        self.aggregation_method = aggregation_method
        self.aggregation_method_params = aggregation_method_params
        self.method = method
        self.method_params = method_params
        self.input = input
        self.contexts = contexts
        super().__init__(alias=alias or f"Ranking for {input} with {contexts}", tests=tests)

    def generate_data(
        self,
        dataset: Dataset,
        options: Options,
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        """Generate relevance scores for input-context pairs."""
        data = dataset.column(self.contexts)

        (method, aggregation_method) = METHODS.get(self.method)
        if method is None:
            raise ValueError(f"Method {self.method} not found")
        if self.aggregation_method is not None:
            aggregation_method = AGGREGATION_METHODS.get(self.aggregation_method)
        if aggregation_method is None:
            raise ValueError(f"Aggregation method {self.aggregation_method} not found")

        scored_contexts = method(dataset.column(self.input), data, options, **(self.method_params or {}))
        aggregation = aggregation_method(**(self.aggregation_method_params or {}))
        aggregated_scores = scored_contexts.data.apply(aggregation.do)
        result = {
            f"{self.alias}": DatasetColumn(ColumnType.Numerical, aggregated_scores),
        }
        if self.output_scores:
            result[f"{self.alias} scores"] = scored_contexts
        return result

    def list_input_columns(self) -> Optional[List[str]]:
        """Return list of required input column names."""
        return [self.input, self.contexts]
