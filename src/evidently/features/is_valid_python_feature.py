import ast
from typing import Any
from typing import ClassVar
from typing import Optional

from evidently.core import ColumnType
from evidently.features.generated_features import ApplyColumnGeneratedFeature


class IsValidPython(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:IsValidPython"

    __feature_type__: ClassVar = ColumnType.Categorical
    display_name_template: ClassVar = "Valid Python for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def apply(self, value: Any) -> bool:
        try:
            ast.parse(value)
            return True
        except (SyntaxError, TypeError):
            return False
