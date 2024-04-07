import uuid
from typing import Optional

import pandas as pd

from openai import OpenAI

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class OpenAIFeature(GeneratedFeature):
    column_name: str
    feature_id: str
    prompt: str
    prompt_replace_string: str
    model: str

    def __init__(
        self,
        column_name: str,
        model: str,
        prompt: str,
        prompt_replace_string: str,
        feature_type: str,
        display_name: Optional[str] = None,
    ):
        self.feature_id = str(uuid.uuid4())
        self.prompt = prompt
        self.prompt_replace_string = prompt_replace_string
        self.model = model
        self.feature_type = ColumnType.Categorical if feature_type == "cat" else ColumnType.Numerical
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        column_data = data[self.column_name]
        client = OpenAI()
        result = []
        for value in column_data:
            prompt = self.prompt.replace(self.prompt_replace_string, value)
            prompt_answer = client.completions.create(model=self.model, prompt=prompt)
            if self.feature_type == "cat":
                result.append(prompt_answer.choices[0].text)
            else:
                try:
                    result.append(float(prompt_answer.choices[0].text))
                except ValueError:
                    result.append(None)

        return pd.DataFrame(dict([(self._feature_column_name(), result)]))

    def feature_name(self) -> ColumnName:
        return additional_feature(
            self,
            self._feature_column_name(),
            self.display_name or f"OpenAI for {self.column_name}",
        )

    def _feature_column_name(self) -> str:
        return self.column_name + "_" + self.feature_id
