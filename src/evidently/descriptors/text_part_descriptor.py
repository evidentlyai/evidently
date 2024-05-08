from evidently.features import text_part_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class TextBegins(FeatureDescriptor):
    prefix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.TextBegins(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        )

    def for_column(self, column_name: str):
        return text_part_feature.TextBegins(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        ).feature_name()


class TextEnds(FeatureDescriptor):
    suffix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.TextEnds(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        )

    def for_column(self, column_name: str):
        return text_part_feature.TextEnds(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        ).feature_name()
