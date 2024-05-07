import uuid
from typing import Optional

import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class HFFeature(GeneratedFeature):
    feature_id: str
    column_name: str
    path: str
    config_name: str
    model_params: dict
    compute_params: dict
    result_scores_field: str

    def __init__(
        self,
        column_name: str,
        path: str,
        config_name: str,
        model_params: dict,
        compute_params: dict,
        result_scores_field: str,
        display_name: Optional[str] = None,
    ):
        self.feature_id = str(uuid.uuid4())
        self.result_scores_field = result_scores_field
        self.path = path
        self.config_name = config_name
        self.model_params = model_params
        self.compute_params = compute_params
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        import evaluate

        column_data = data[self.column_name].values.tolist()
        model = evaluate.load(
            self.path,
            self.config_name,
            **self.model_params,
        )
        scores = model.compute(predictions=column_data, **self.compute_params)
        return pd.DataFrame(dict([(self._feature_column_name(), scores[self.result_scores_field])]), index=data.index)

    def feature_name(self) -> ColumnName:
        return additional_feature(
            self,
            self._feature_column_name(),
            self.display_name or f"Hugging Face % for {self.column_name}",
        )

    def _feature_column_name(self) -> str:
        if self.display_name:
            return self.display_name.replace(" ", "_").lower()
        return self.column_name + "_" + self.feature_id
