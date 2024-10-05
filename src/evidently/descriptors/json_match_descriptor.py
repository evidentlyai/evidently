from evidently.features import json_match_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class JSONMatch(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:JSONMatch"

    # func: Callable[[pd.Series, pd.Series], pd.Series]
    display_name: str
    with_column: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return json_match_feature.JSONMatch(
            first_column=column_name, second_column=self.with_column, display_name=self.display_name
        )
