from typing import Dict
from typing import Optional
from typing import Union

from evidently import ColumnType
from evidently.v2.datasets import Dataset
from evidently.v2.datasets import DatasetColumn
from evidently.v2.datasets import Scorer


class TextLength(Scorer):
    def __init__(self, column_name: str, alias: Optional[str] = None):
        super().__init__(alias)
        self._column_name: str = column_name

    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        column_items_lengths = dataset.as_dataframe()[self._column_name].apply(len)
        return DatasetColumn(type=ColumnType.Numerical, data=column_items_lengths)
