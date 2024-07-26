import re
from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np

from evidently.features.generated_features import ApplyColumnGeneratedFeature


class SentenceCount(ApplyColumnGeneratedFeature):
    _reg: ClassVar[re.Pattern] = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
    display_name_template: ClassVar = "Sentence Count for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        number = len(self._reg.split(value))
        return max(1, number)
