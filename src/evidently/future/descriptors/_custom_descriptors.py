from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import Descriptor
from evidently.options.base import Options


class CustomColumnDescriptor(Descriptor):
    def __init__(self, column_name: str, func: Callable[[DatasetColumn], DatasetColumn], alias: Optional[str] = None):
        super().__init__(alias or f"custom_column_descriptor:{func.__name__}")
        self._column_name = column_name
        self._func = func

    def generate_data(self, dataset: Dataset, options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        column_data = dataset.column(self._column_name)
        return self._func(column_data)


class CustomDescriptor(Descriptor):
    def __init__(
        self, func: Callable[[Dataset], Union[DatasetColumn, Dict[str, DatasetColumn]]], alias: Optional[str] = None
    ):
        super().__init__(alias or f"custom_descriptor:{func.__name__}")
        self._func = func

    def generate_data(self, dataset: "Dataset", options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        return self._func(dataset)
