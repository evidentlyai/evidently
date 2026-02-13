from typing import ClassVar
from typing import Optional

from evidently.legacy.features import is_valid_python_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class IsValidPython(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:IsValidPython"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_python_feature.IsValidPython(column_name, self.display_name)
