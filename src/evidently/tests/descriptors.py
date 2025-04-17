from typing import Any

import pandas as pd

from evidently.core.datasets import DescriptorTest


class EqualsDescriptorTest(DescriptorTest):
    expected: Any

    def apply(self, row: pd.Series) -> bool:
        return any(r == self.expected for r in row)
