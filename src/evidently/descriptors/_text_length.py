from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import numpy as np

from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.legacy.core import ColumnType
from evidently.legacy.options.base import Options


class TextLength(Descriptor):
    column_name: str

    def __init__(self, column_name: str, alias: Optional[str] = None):
        self.column_name: str = column_name
        super().__init__(alias=alias or "text_length")

    def generate_data(self, dataset: "Dataset", options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        column_items_lengths = dataset.as_dataframe()[self.column_name].apply(_apply)
        return DatasetColumn(type=ColumnType.Numerical, data=column_items_lengths)


def _apply(value: Any):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0
    return len(value)
