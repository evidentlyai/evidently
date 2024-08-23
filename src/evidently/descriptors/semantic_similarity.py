from typing import List

from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.generated_features import MultiColumnFeatureDescriptor
from evidently.features.semantic_similarity_feature import SemanticSimilarityFeature


class SemanticSimilarity(MultiColumnFeatureDescriptor):
    def feature(self, columns: List[str]) -> GeneratedFeature:
        return SemanticSimilarityFeature(columns=columns, display_name=self.display_name)


class SemanticSimilatiryDescriptor(FeatureDescriptor):
    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return SemanticSimilarityFeature(columns=[column_name, self.with_column], display_name=self.display_name)
