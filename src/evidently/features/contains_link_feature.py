from typing import Any
from typing import ClassVar
from typing import Optional
from urllib.parse import urlparse

import numpy as np

from evidently import ColumnType
from evidently.features.generated_features import ApplyColumnGeneratedFeature


class ContainsLink(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:ContainsLink"

    __feature_type__: ClassVar = ColumnType.Categorical
    display_name_template: ClassVar = "{column_name} contains link"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        # Split the text into words
        words = str(value).split()

        # Check if any word is a valid URL using urlparse
        for word in words:
            parsed = urlparse(word)
            if parsed.scheme and parsed.netloc:
                return True
        return False
