from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

from evidently.legacy.core import Label


class TaskType:
    REGRESSION_TASK: str = "regression"
    CLASSIFICATION_TASK: str = "classification"
    RECOMMENDER_SYSTEMS: str = "recsys"


class RecomType(str, Enum):
    SCORE = "score"
    RANK = "rank"


TargetNames = Union[List[Label], Dict[Label, str]]
Embeddings = Dict[str, List[str]]
_FEATURE_LIST_FIELDS = frozenset({"numerical_features", "categorical_features", "datetime_features", "text_features"})


@dataclass
class ColumnMapping:
    target: Optional[str] = "target"
    prediction: Optional[Union[str, int, Union[Sequence[str], Sequence[int]]]] = "prediction"
    datetime: Optional[str] = "datetime"
    id: Optional[str] = None
    numerical_features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    datetime_features: Optional[List[str]] = None
    target_names: Optional[TargetNames] = None
    task: Optional[str] = None
    pos_label: Optional[Union[str, int]] = 1
    text_features: Optional[List[str]] = None
    embeddings: Optional[Embeddings] = None
    user_id: Optional[str] = "user_id"
    item_id: Optional[str] = "item_id"
    recommendations_type: Union[RecomType, str] = RecomType.SCORE

    def __setattr__(self, name: str, value: object) -> None:
        # A lone column name is a str. Leaving it as a str makes `name in features`
        # a substring test, so "prediction" matches "prediction_timestamp_utc" and
        # is typed as a datetime feature (#846).
        if name in _FEATURE_LIST_FIELDS and isinstance(value, str):
            value = [value]
        object.__setattr__(self, name, value)

    @property
    def recom_type(self) -> RecomType:
        if isinstance(self.recommendations_type, str):
            return RecomType(self.recommendations_type)
        return self.recommendations_type

    def is_classification_task(self) -> bool:
        return self.task == TaskType.CLASSIFICATION_TASK

    def is_regression_task(self) -> bool:
        return self.task == TaskType.REGRESSION_TASK
