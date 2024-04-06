from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.hf_feature import HFFeature


class HuggingFaceModel(FeatureDescriptor):
    def for_column(self, column_name: str):
        return HFFeature(column_name).feature_name()

    def feature(self, column_name: str) -> GeneratedFeature:
        return HFFeature(column_name)
