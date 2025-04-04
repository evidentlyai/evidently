from evidently.legacy.features.BERTScore_feature import BERTScoreFeature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeatures


class BERTScore(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:BERTScore"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return BERTScoreFeature(columns=[column_name, self.with_column], display_name=self.display_name)
