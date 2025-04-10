from evidently.legacy.features import regexp_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class RegExp(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:RegExp"

    reg_exp: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return regexp_feature.RegExp(column_name, self.reg_exp, self.display_name)
