from evidently.legacy.features.exact_match_feature import ExactMatchFeature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeatures


class ExactMatch(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:ExactMatch"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return ExactMatchFeature(columns=[column_name, self.with_column], display_name=self.display_name)
