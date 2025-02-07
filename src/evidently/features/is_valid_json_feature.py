import json
from typing import Any
from typing import ClassVar
from typing import Optional

from evidently.core import ColumnType
from evidently.features.generated_features import ApplyColumnGeneratedFeature


class IsValidJSON(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:IsValidJSON"

    __feature_type__: ClassVar = ColumnType.Categorical
    display_name_template: ClassVar = "JSON valid for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def apply(self, value: Any):
        try:
            json.loads(value)
        except ValueError:
            return False
        return True
