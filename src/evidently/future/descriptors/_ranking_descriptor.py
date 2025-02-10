from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from evidently import ColumnType
from evidently.base_metric import DisplayName
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import Descriptor


def semantic_similarity_scoring(question: DatasetColumn, context: DatasetColumn) -> DatasetColumn:
    from sentence_transformers import SentenceTransformer

    model_id: str = "all-MiniLM-L6-v2"

    def normalized_cosine_distance(left, right):
        return 1 - ((1 - np.dot(left, right) / (np.linalg.norm(left) * np.linalg.norm(right))) / 2)

    model = SentenceTransformer(model_id)
    context_column = context.data.name
    no_index_context = context.data.reset_index()

    first = model.encode(question.data.fillna(""))
    context_rows = no_index_context[context_column].explode().reset_index()
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


def mean(scores: List[float]) -> float:
    return np.average(scores)


METHODS = {
    "semantic_similarity": (semantic_similarity_scoring, mean),
}


AGGREGATION_METHODS = {
    "mean": mean,
}


class RankingDescriptor(Descriptor):
    def __init__(
        self,
        question: str,
        context: str,
        method: str = "semantic_similarity",
        aggregation_method: Optional[str] = None,
        output_scores: bool = False,
        alias: Optional[str] = None,
    ):
        super().__init__(alias or f"Ranking for {question} with {context}")
        self.output_scores = output_scores
        self.aggregation_method = aggregation_method
        self.method = method
        self.question = question
        self.context = context

    def generate_data(self, dataset: Dataset) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        data = dataset.column(self.context)

        (method, aggregation_method) = METHODS.get(self.method)
        if method is None:
            raise ValueError(f"Method {self.method} not found")
        if self.aggregation_method is not None:
            aggregation_method = AGGREGATION_METHODS.get(self.aggregation_method)
        if aggregation_method is None:
            raise ValueError(f"Aggregation method {self.aggregation_method} not found")

        scored_contexts = method(dataset.column(self.question), data)
        aggregated_scores = scored_contexts.data.apply(aggregation_method)
        result = {
            f"{self.alias}: aggregate score": DatasetColumn(ColumnType.Numerical, aggregated_scores),
        }
        if self.output_scores:
            result[f"{self.alias}: scores"] = scored_contexts
        return result
