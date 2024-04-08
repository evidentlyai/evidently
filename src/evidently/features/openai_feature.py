import uuid
from typing import List
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
    context: str
    context_replace_string: str
    openai_params: dict
    model: str
    possible_values: Optional[List[str]]

    def __init__(
        self,
        column_name: str,
        model: str,
        prompt: str,
        feature_type: str,
        context: str = "",
        prompt_replace_string: str = "REPLACE",
        context_replace_string: str = "CONTEXT",
        possible_values: Optional[List[str]] = None,
        openai_params: Optional[dict] = None,
        display_name: Optional[str] = None,
    ):
        self.feature_id = str(uuid.uuid4())
        self.prompt = prompt
        self.prompt_replace_string = prompt_replace_string
        self.context = context
        self.context_replace_string = context_replace_string
        self.openai_params = openai_params or {}
        self.model = model
        self.feature_type = ColumnType.Categorical if feature_type == "cat" else ColumnType.Numerical
        self.column_name = column_name
        self.display_name = display_name
        self.possible_values = [v.upper for v in possible_values] if possible_values else None
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        column_data = data[self.column_name]
        client = OpenAI()
        result = []
        prompt = self.prompt.replace(self.context_replace_string, self.context)
        for value in column_data:
            prompt = prompt.replace(self.prompt_replace_string, value)
            prompt_answer = client.completions.create(model=self.model, prompt=prompt, **self.openai_params)
            processed_response = _postprocess_response(prompt_answer.choices[0].text, self.possible_values)
            if self.feature_type == "cat":
                result.append(processed_response)
            else:
                try:
                    result.append(float(processed_response))
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


def _postprocess_response(response: str, possible_values: List[str]) -> Optional[str]:
    for line in response.split("\n"):
        line = line.strip().upper()
        if line:
            if possible_values:
                if line in possible_values:
                    return line
                else:
                    return None
            return line
    return None
