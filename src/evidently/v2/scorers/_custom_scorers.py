from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from evidently.v2.datasets import Dataset
from evidently.v2.datasets import DatasetColumn
from evidently.v2.datasets import Scorer


class CustomColumnScorer(Scorer):
    def __init__(self, column_name: str, func: Callable[[DatasetColumn], DatasetColumn], alias: Optional[str] = None):
        super().__init__(alias)
        self._column_name = column_name
        self._func = func

    def generate_data(self, dataset: Dataset) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        column_data = dataset.column(self._column_name)
        return self._func(column_data)


class CustomScorer(Scorer):
    def __init__(
        self, func: Callable[[Dataset], Union[DatasetColumn, Dict[str, DatasetColumn]]], alias: Optional[str] = None
    ):
        super().__init__(alias)
        self._func = func

    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        return self._func(dataset)
