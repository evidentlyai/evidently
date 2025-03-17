from typing import ClassVar

from evidently.features import regexp_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class RegExp(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:RegExp"

    reg_exp: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return regexp_feature.RegExp(column_name, self.reg_exp, self.display_name)
