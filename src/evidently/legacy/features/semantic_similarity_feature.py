from typing import ClassVar
from typing import List

import numpy as np
import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class SemanticSimilarityFeature(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:SemanticSimilarityFeature"

    __feature_type__: ClassVar = ColumnType.Numerical
    columns: List[str]
    model: str = "all-MiniLM-L6-v2"

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        from sentence_transformers import SentenceTransformer

        def normalized_cosine_distance(left, right):
            return 1 - ((1 - np.dot(left, right) / (np.linalg.norm(left) * np.linalg.norm(right))) / 2)

        model = SentenceTransformer(self.model)

        first = model.encode(data[self.columns[0]].fillna(""))
        second = model.encode(data[self.columns[1]].fillna(""))

        return pd.DataFrame(
            {
                self._feature_name(): pd.Series(
                    [normalized_cosine_distance(x, y) for x, y in zip(first, second)],
                    index=data.index,
                )
            }
        )

    def _feature_name(self):
        return "|".join(self.columns)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"Semantic Similarity for {' '.join(self.columns)}.",
        )
