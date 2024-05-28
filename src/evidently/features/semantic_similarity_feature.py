from typing import List
from typing import Optional

import pandas as pd

from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class SemanticSimilarityFeature(GeneratedFeature):
    columns: List[str]
    feature_type = ColumnType.Numerical
    model: str = "all-MiniLM-L6-v2"

    def __init__(self, columns: List[str], display_name: Optional[str] = None):
        self.columns = columns
        self.display_name = display_name or f"Semantic Similarity for {' '.join(columns)}."
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        from scipy.spatial import distance
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(self.model)

        first = model.encode(data[self.columns[0]].fillna(""))
        second = model.encode(data[self.columns[1]].fillna(""))

        return pd.Series([distance.cosine(x, y) for x, y in zip(first, second)], index=data.index)
