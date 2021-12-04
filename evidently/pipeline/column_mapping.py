from typing import Optional, List, Union, Sequence

from dataclasses import dataclass


@dataclass
class ColumnMapping:
    target: Optional[str] = "target"
    prediction: Optional[Union[str, Sequence[str]]] = "prediction"
    datetime: Optional[str] = "datetime"
    id: Optional[str] = None
    numerical_features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    target_names: Optional[List[str]] = None
