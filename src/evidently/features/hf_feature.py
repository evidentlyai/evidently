import uuid
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.core import ColumnType
from evidently.features.generated_features import DataFeature
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


class GeneralHuggingFaceFeature(DataFeature):
    column_name: str
    model: str
    params: dict

    def __init__(self, *, column_name: str, model: str, params: dict, display_name: str):
        self.column_name = column_name
        self.model = model
        self.params = params
        self.display_name = display_name
        self.feature_type = _model_type(model)
        super().__init__()

    def generate_data(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        _, available_params, func = _models.get(self.model, (ColumnType.Unknown, [], None))
        if func is None:
            raise ValueError(f"Model {self.model} not found. Available models: {', '.join(_models.keys())}")
        result = func(data[self.column_name], **{param: self.params.get(param, None) for param in available_params})
        return result


def _samlowe_roberta_base_go_emotions(data: pd.Series, label: str) -> pd.Series:
    from transformers import pipeline

    def _convert_labels(row):
        return {x["label"]: x["score"] for x in row}

    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    model_outputs = classifier(data.fillna("").tolist())
    return pd.Series([_convert_labels(out).get(label, None) for out in model_outputs], index=data.index)


def _openai_detector(data: pd.Series, score_threshold: float) -> pd.Series:
    from transformers import pipeline

    def _get_label(row):
        return row["label"] if row["score"] > score_threshold else "Unknown"

    pipe = pipeline("text-classification", model="roberta-base-openai-detector")
    return pd.Series([_get_label(x) for x in pipe(data.fillna("").tolist())], index=data.index)


def _lmnli_fever(data: pd.Series, labels: List[str]) -> pd.Series:
    from transformers import pipeline

    classifier = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
    )
    output = classifier(data.fillna("").tolist(), labels, multi_label=False)
    return pd.Series(output, index=data.index)


def _model_type(model: str) -> ColumnType:
    return _models.get(model, (ColumnType.Unknown, None, None))[0]


_models: Dict[str, Tuple[ColumnType, List[str], Callable[..., pd.Series]]] = {
    "SamLowe/roberta-base-go_emotions": (ColumnType.Numerical, ["label"], _samlowe_roberta_base_go_emotions),
    "openai-community/roberta-base-openai-detector": (ColumnType.Categorical, ["score_threshold"], _openai_detector),
    "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli": (
        ColumnType.Categorical,
        ["labels"],
        _lmnli_fever,
    ),
}
