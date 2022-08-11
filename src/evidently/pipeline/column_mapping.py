from typing import Optional, List, Union, Sequence

from dataclasses import dataclass


@dataclass
class ColumnMapping:
    REGRESSION_TASK: str = "regression"
    CLASSIFICATION_TASK: str = "classification"
    target: Optional[str] = "target"
    prediction: Optional[Union[str, Sequence[str]]] = "prediction"
    datetime: Optional[str] = "datetime"
    id: Optional[str] = None
    numerical_features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    datetime_features: Optional[List[str]] = None
    target_names: Optional[List[str]] = None
    task: Optional[str] = None
    pos_label: Optional[Union[str, int]] = 1

    def is_classification_task(self):
        return self.task == self.CLASSIFICATION_TASK

    def is_regression_task(self):
        return self.task == self.is_regression_task()
