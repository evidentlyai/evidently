from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently.core.datasets import AnyDescriptorTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.legacy.core import ColumnType
from evidently.legacy.options.base import Options

VALID_ROUGE_TYPES = ("rouge1", "rouge2", "rougeL", "rougeLsum")
VALID_SCORE_TYPES = ("f", "precision", "recall")


class RougeScore(Descriptor):
    """Compute ROUGE score between a prediction column and a reference column, row by row.

    ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measures n-gram
    overlap between generated text and reference text. Returns a numeric score
    in [0, 1] for each row.

    Requires the ``rouge-score`` package (``pip install evidently[llm]``).

    Args:
        prediction_column: Column containing generated/predicted text.
        reference_column: Column containing the reference/ground-truth text.
        rouge_type: ROUGE variant — ``'rouge1'`` (unigrams), ``'rouge2'`` (bigrams),
            or ``'rougeL'`` (longest common subsequence). Default ``'rouge1'``.
        score_type: Which score component to return — ``'f'`` (F1, default),
            ``'precision'``, or ``'recall'``.
        alias: Optional display name for the resulting column.
        tests: Optional pass/fail conditions on the score.

    Example::

        from evidently.descriptors import RougeScore

        RougeScore("response", "ground_truth", rouge_type="rouge1", alias="ROUGE-1")
    """

    prediction_column: str
    reference_column: str
    rouge_type: str = "rouge1"
    score_type: str = "f"

    def __init__(
        self,
        prediction_column: str,
        reference_column: str,
        rouge_type: str = "rouge1",
        score_type: str = "f",
        alias: Optional[str] = None,
        tests: Optional[List[AnyDescriptorTest]] = None,
    ):
        if rouge_type not in VALID_ROUGE_TYPES:
            raise ValueError(f"rouge_type must be one of {VALID_ROUGE_TYPES}, got '{rouge_type}'")
        if score_type not in VALID_SCORE_TYPES:
            raise ValueError(f"score_type must be one of {VALID_SCORE_TYPES}, got '{score_type}'")
        self.prediction_column = prediction_column
        self.reference_column = reference_column
        self.rouge_type = rouge_type
        self.score_type = score_type
        default_alias = f"{rouge_type}_{score_type}({prediction_column},{reference_column})"
        super().__init__(alias=alias or default_alias, tests=tests)

    def generate_data(
        self,
        dataset: Dataset,
        options: Options,
    ) -> Union[DatasetColumn, dict]:
        from rouge_score import rouge_scorer

        scorer = rouge_scorer.RougeScorer([self.rouge_type], use_stemmer=False)
        df = dataset.as_dataframe()

        scores = []
        for pred, ref in zip(
            df[self.prediction_column].fillna("").tolist(),
            df[self.reference_column].fillna("").tolist(),
        ):
            result = scorer.score(str(ref), str(pred))
            score_obj = result[self.rouge_type]
            if self.score_type == "f":
                scores.append(score_obj.fmeasure)
            elif self.score_type == "precision":
                scores.append(score_obj.precision)
            else:
                scores.append(score_obj.recall)

        return DatasetColumn(
            type=ColumnType.Numerical,
            data=pd.Series(scores, index=df.index),
        )

    def list_input_columns(self) -> Optional[List[str]]:
        return [self.prediction_column, self.reference_column]
