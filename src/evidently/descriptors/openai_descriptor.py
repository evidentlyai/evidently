from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.openai_feature import OpenAIFeature


class OpenAIPrompting(FeatureDescriptor):
    prompt: str
    prompt_replace_string: str
    model: str
    feature_type: str

    def __init__(self, prompt: str, prompt_replace_string: str, model: str, feature_type: str):
        self.model = model
        self.feature_type = feature_type
        self.prompt_replace_string = prompt_replace_string
        self.prompt = prompt
        super().__init__()

    def for_column(self, column_name: str):
        return OpenAIFeature(
            column_name,
            model=self.model,
            prompt=self.prompt,
            prompt_replace_string=self.prompt_replace_string,
            feature_type=self.feature_type,
        ).feature_name()

    def feature(self, column_name: str) -> GeneratedFeature:
        return OpenAIFeature(
            column_name,
            model=self.model,
            prompt=self.prompt,
            prompt_replace_string=self.prompt_replace_string,
            feature_type=self.feature_type,
        )
