from evidently.features import contains_link_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class ContainsLink(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:ContainsLink"

    def feature(self, column_name: str) -> GeneratedFeature:
        return contains_link_feature.ContainsLink(column_name, self.display_name)
