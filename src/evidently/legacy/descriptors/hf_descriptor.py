from typing import Optional

from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.features.hf_feature import HuggingFaceFeature
from evidently.legacy.features.hf_feature import HuggingFaceToxicityFeature


class HuggingFaceModel(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:HuggingFaceModel"

    model: str
    params: Optional[dict] = None

    def feature(self, column_name: str) -> GeneratedFeature:
        return HuggingFaceFeature(
            column_name=column_name,
            model=self.model,
            params=self.params or {},
            display_name=self.display_name or f"Hugging Face Model ({self.model}) for {column_name}",
        )


class HuggingFaceToxicityModel(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:HuggingFaceToxicityModel"

    model: Optional[str] = None
    toxic_label: Optional[str] = None

    def feature(self, column_name: str) -> GeneratedFeature:
        model_str = "" if self.model is None else f"({self.model})"
        return HuggingFaceToxicityFeature(
            column_name=column_name,
            display_name=self.display_name or f"Hugging Face Toxicity {model_str} for {column_name}",
            model=self.model,
            toxic_label=self.toxic_label,
        )
