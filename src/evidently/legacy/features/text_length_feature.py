from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np

from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature


class TextLength(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:TextLength"

    __feature_type__: ClassVar = ColumnType.Numerical
    display_name_template: ClassVar = "Text Length for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.display_name = display_name
        super().__init__(column_name=column_name)

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        return len(value)
