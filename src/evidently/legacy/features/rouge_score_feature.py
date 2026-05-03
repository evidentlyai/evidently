from typing import ClassVar
from typing import List

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition

VALID_ROUGE_TYPES = ("rouge1", "rouge2", "rougeL", "rougeLsum")
VALID_SCORE_TYPES = ("f", "precision", "recall")


class RougeScoreFeature(GeneratedFeature):
    """Compute ROUGE score between two text columns row by row.

    ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measures
    n-gram overlap between a generated text (prediction) and a reference text.

    Requires the ``rouge-score`` package (``pip install evidently[llm]``).
    """

    class Config:
        type_alias = "evidently:feature:RougeScoreFeature"

    __feature_type__: ClassVar = ColumnType.Numerical

    columns: List[str]
    """Two-element list: [prediction_column, reference_column]."""

    rouge_type: str = "rouge1"
    """ROUGE variant to compute: 'rouge1', 'rouge2', 'rougeL', or 'rougeLsum'."""

    score_type: str = "f"
    """Which score to return: 'f' (F1), 'precision', or 'recall'."""

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        from rouge_score import rouge_scorer

        if self.rouge_type not in VALID_ROUGE_TYPES:
            raise ValueError(f"rouge_type must be one of {VALID_ROUGE_TYPES}, got '{self.rouge_type}'")
        if self.score_type not in VALID_SCORE_TYPES:
            raise ValueError(f"score_type must be one of {VALID_SCORE_TYPES}, got '{self.score_type}'")

        scorer = rouge_scorer.RougeScorer([self.rouge_type], use_stemmer=False)
        prediction_col, reference_col = self.columns[0], self.columns[1]

        scores = []
        for pred, ref in zip(
            data[prediction_col].fillna("").tolist(),
            data[reference_col].fillna("").tolist(),
        ):
            result = scorer.score(str(ref), str(pred))
            score_obj = result[self.rouge_type]
            if self.score_type == "f":
                scores.append(score_obj.fmeasure)
            elif self.score_type == "precision":
                scores.append(score_obj.precision)
            else:
                scores.append(score_obj.recall)

        return pd.DataFrame(
            {self._feature_name(): pd.Series(scores, index=data.index)}
        )

    def _feature_name(self) -> str:
        return "|".join(self.columns) + f"|{self.rouge_type}|{self.score_type}"

    def _as_column(self) -> "ColumnName":
        pred, ref = self.columns[0], self.columns[1]
        display = f"{self.rouge_type.upper()} ({self.score_type}) for {pred} vs {ref}"
        return self._create_column(self._feature_name(), default_display_name=display)
