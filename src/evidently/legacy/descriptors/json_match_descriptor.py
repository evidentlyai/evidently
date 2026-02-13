from typing import ClassVar
from typing import Optional

from evidently.legacy.features import json_match_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class JSONMatch(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:JSONMatch"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return json_match_feature.JSONMatch(first_column=column_name, second_column=self.with_column)
