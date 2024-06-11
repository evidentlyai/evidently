from typing import List

import pandas as pd
import numpy as np

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class SemanticSimilarityFeature(GeneratedFeature):
    columns: List[str]
    feature_type = ColumnType.Numerical
    model: str = "all-MiniLM-L6-v2"

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        from sentence_transformers import SentenceTransformer

        def normalized_cosine_distance(left: np.array, right: np.array) -> float:
            return 1 - ((1 - np.dot(left, right) / (np.linalg.norm(left) * np.linalg.norm(right))) / 2)

        model = SentenceTransformer(self.model)

        first = model.encode(data[self.columns[0]].fillna(""))
        second = model.encode(data[self.columns[1]].fillna(""))

        return pd.DataFrame(
            dict(
                [
                    (
                        "|".join(self.columns),
                        pd.Series(
                            [normalized_cosine_distance(left=x, right=y) for x, y in zip(first, second)],
                            index=data.index,
                        ),
                    )
                ]
            )
        )

    def feature_name(self) -> "ColumnName":
        return additional_feature(
            self,
            "|".join(self.columns),
            self.display_name or f"Semantic Similarity for {' '.join(self.columns)}.",
        )
