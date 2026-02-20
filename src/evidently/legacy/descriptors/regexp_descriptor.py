from typing import ClassVar
from typing import Optional

from evidently.legacy.features import regexp_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class RegExp(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:RegExp"

    reg_exp: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return regexp_feature.RegExp(column_name, self.reg_exp, self.display_name)
