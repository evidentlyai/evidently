from typing import Any
from typing import ClassVar
from typing import Optional

from evidently.core import ColumnType
from evidently.features.generated_features import ApplyColumnGeneratedFeature


class IsValidSQL(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:IsValidSQL"

    __feature_type__: ClassVar = ColumnType.Categorical
    display_name_template: ClassVar = "SQL Validity Check for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def apply(self, value: Any):
        if value is None or not isinstance(value, str):
            return False

        return self.is_valid_sql(value)

    def is_valid_sql(self, query: str) -> bool:
        import sqlvalidator

        queries = query.strip().split(";")  # Split by semicolon

        for q in queries:
            q = q.strip()  # Remove extra whitespace
            if not q:  # Skip empty queries
                continue

            try:
                sqlvalidator.format_sql(q)  # Validate SQL syntax
            except Exception:
                return False  # Invalid SQL

        return True  # All queries are valid
