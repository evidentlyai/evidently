from typing import ClassVar
from typing import Optional

from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.features.semantic_similarity_feature import SemanticSimilarityFeature


class SemanticSimilarity(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:SemanticSimilarity"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return SemanticSimilarityFeature(columns=[column_name, self.with_column], display_name=self.display_name)
