from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import numpy as np

from evidently.core import ColumnType
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import Descriptor
from evidently.options.base import Options


class TextLength(Descriptor):
    def __init__(self, column_name: str, alias: Optional[str] = None):
        super().__init__(alias or "text_length")
        self._column_name: str = column_name

    def generate_data(self, dataset: "Dataset", options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        column_items_lengths = dataset.as_dataframe()[self._column_name].apply(_apply)
        return DatasetColumn(type=ColumnType.Numerical, data=column_items_lengths)


def _apply(value: Any):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0
    return len(value)
