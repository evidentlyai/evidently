from evidently.features import sentence_count_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class SentenceCount(FeatureDescriptor):
    def feature(self, column_name: str) -> GeneratedFeature:
        return sentence_count_feature.SentenceCount(column_name, self.display_name)
