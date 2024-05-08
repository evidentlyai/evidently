from evidently.features import text_part_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class TextBeginsWith(FeatureDescriptor):
    prefix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.TextBeginsWith(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        )

    def for_column(self, column_name: str):
        return text_part_feature.TextBeginsWith(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        ).feature_name()


class TextEndsWith(FeatureDescriptor):
    suffix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.TextEndsWith(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        )

    def for_column(self, column_name: str):
        return text_part_feature.TextEndsWith(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        ).feature_name()
