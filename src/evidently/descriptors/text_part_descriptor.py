from evidently.features import text_part_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class TextPart(FeatureDescriptor):
    substring: str
    mode: str = "prefix"
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.TextPart(
            column_name,
            self.substring,
            self.case_sensitive,
            self.mode,
            self.display_name,
        )

    def for_column(self, column_name: str):
        return text_part_feature.TextPart(
            column_name,
            self.substring,
            self.case_sensitive,
            self.mode,
            self.display_name,
        ).feature_name()
