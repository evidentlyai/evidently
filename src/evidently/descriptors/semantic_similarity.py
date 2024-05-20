from typing import List

from evidently.features.generated_features import GeneralDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.semantic_similarity_feature import SemanticSimilarityFeature


class SemanticSimilarity(GeneralDescriptor):
    columns: List[str]

    def feature(self) -> GeneratedFeature:
        return SemanticSimilarityFeature(columns=self.columns, display_name=self.display_name)
