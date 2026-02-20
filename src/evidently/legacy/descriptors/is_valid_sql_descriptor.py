from typing import ClassVar
from typing import Optional

from evidently.legacy.features import is_valid_sql_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class IsValidSQL(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:IsValidSQL"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_sql_feature.IsValidSQL(column_name, self.display_name)
