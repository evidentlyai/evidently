from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union


class TaskType:
    REGRESSION_TASK: str = "regression"
    CLASSIFICATION_TASK: str = "classification"


TargetNames = Union[List[int], List[str], Dict[int, str], Dict[str, str]]


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

    def is_classification_task(self):
        return self.task == TaskType.CLASSIFICATION_TASK

    def is_regression_task(self):
        return self.task == TaskType.REGRESSION_TASK
