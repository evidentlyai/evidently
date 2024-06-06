from typing import Optional

from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.hf_feature import GeneralHuggingFaceFeature
from evidently.features.hf_feature import HFFeature
from evidently.features.hf_feature import HuggingFaceToxicityFeature


class HuggingFaceModel(FeatureDescriptor):
    path: str
    config_name: str
    model_params: dict
    compute_params: dict
    result_scores_field: str

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


class GeneralHuggingFaceModel(FeatureDescriptor):
    model: str
    params: Optional[dict] = None

    def feature(self, column_name: str) -> GeneratedFeature:
        return GeneralHuggingFaceFeature(
            column_name=column_name,
            model=self.model,
            params=self.params or {},
            display_name=self.display_name or f"Hugging Face Model ({self.model}) for {column_name}",
        )


class HuggingFaceToxicityModel(FeatureDescriptor):
    model: Optional[str] = None
    toxic_label: Optional[str] = None

    def feature(self, column_name: str) -> GeneratedFeature:
        model_str = "" if self.model is None else f"({self.model})"
        return HuggingFaceToxicityFeature(
            column_name=column_name,
            display_name=f"Hugging Face Toxicity {model_str} for {column_name}",
            model=self.model,
            toxic_label=self.toxic_label,
        )
