from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.semantic_similarity_feature import SemanticSimilarityFeature


class SemanticSimilarity(FeatureDescriptor):
    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return SemanticSimilarityFeature(columns=[column_name, self.with_column], display_name=self.display_name)
