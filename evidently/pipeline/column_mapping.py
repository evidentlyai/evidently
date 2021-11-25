from typing import Optional, List

from dataclasses import dataclass


@dataclass
class ColumnMapping:
    target: str = "target"
    prediction: str = "prediction"
    datetime: str = "datetime"
    id: Optional[str] = None
    numerical_features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    target_names: Optional[List[str]] = None
