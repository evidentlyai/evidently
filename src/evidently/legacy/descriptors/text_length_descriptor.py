from evidently.legacy.features import text_length_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class TextLength(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:TextLength"

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_length_feature.TextLength(column_name, self.display_name)
