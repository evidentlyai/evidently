import json
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class JSONSchemaMatch(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:JSONSchemaMatch"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    expected_schema: Dict[str, Type]
    validate_types: bool
    exact_match: bool

    def __init__(
        self,
        column_name: str,
        expected_schema: Dict[str, Type],
        validate_types: bool = False,
        exact_match: bool = False,
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.validate_types = validate_types if not exact_match else True
        self.expected_schema = expected_schema
        self.exact_match = exact_match
        self.display_name = display_name
        super().__init__()

    def _feature_column_name(self) -> str:
        match_type = "exact" if self.exact_match else "minimal"
        return f"{self.column_name}_json_schema_{match_type}_match"

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        calculated = data.apply(lambda row: self.match_json_schema(row[self.column_name]), axis=1)
        return pd.DataFrame({self._feature_column_name(): calculated})

    def match_json_schema(self, json_text: str) -> bool:
        try:
            json_obj = json.loads(json_text)
        except json.JSONDecodeError:
            return False

        if self.exact_match:
            return self._exact_match(json_obj)
        else:
            return self._minimal_match(json_obj)

    def _minimal_match(self, json_obj: Dict) -> bool:
        for key, expected_type in self.expected_schema.items():
            if key not in json_obj or json_obj[key] is None:
                return False
            if self.validate_types and expected_type and not isinstance(json_obj[key], expected_type):
                return False
        return True

    def _exact_match(self, json_obj: Dict) -> bool:
        if set(json_obj.keys()) != set(self.expected_schema.keys()):
            return False
        return self._minimal_match(json_obj)

    def _as_column(self) -> ColumnName:
        match_type = "exact" if self.exact_match else "minimal"
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"JSONSchemaMatch {match_type} match",
        )
