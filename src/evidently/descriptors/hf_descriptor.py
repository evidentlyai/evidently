from typing import Optional

from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.hf_feature import HFFeature


class HuggingFaceModel(FeatureDescriptor):
    path: str
    config_name: str
    model_params: dict
    compute_params: dict
    result_scores_field: str

    def __init__(
        self,
        path: str,
        config_name: str,
        model_params: dict,
        compute_params: dict,
        result_scores_field: str,
        display_name: Optional[str] = None,
    ):
        self.result_scores_field = result_scores_field
        self.compute_params = compute_params
        self.model_params = model_params
        self.config_name = config_name
        self.path = path
        self.display_name = display_name
        super().__init__()

    def for_column(self, column_name: str):
        return HFFeature(
            column_name,
            self.path,
            self.config_name,
            self.model_params,
            self.compute_params,
            self.result_scores_field,
            self.display_name,
        ).feature_name()

    def feature(self, column_name: str) -> GeneratedFeature:
        return HFFeature(
            column_name,
            self.path,
            self.config_name,
            self.model_params,
            self.compute_params,
            self.result_scores_field,
            self.display_name,
        )
