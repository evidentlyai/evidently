from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from evidently._pydantic_compat import PrivateAttr
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import Descriptor
from evidently.options.base import Options

CustomColumnCallable = Callable[[DatasetColumn], DatasetColumn]


class CustomColumnDescriptor(Descriptor):
    column_name: str
    func: str
    _func: Optional[CustomColumnCallable] = PrivateAttr(None)

    def __init__(self, column_name: str, func: Union[str, CustomColumnCallable], alias: Optional[str] = None):
        self.column_name = column_name
        if callable(func):
            self._func = func
            self.func = f"{func.__module__}.{func.__name__}"
        else:
            self._func = None
            self.func = func
        super().__init__(alias=alias or f"custom_column_descriptor:{func}")

    def generate_data(self, dataset: Dataset, options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        if self._func is None:
            raise ValueError("CustomColumnDescriptor is not configured with callable func")
        column_data = dataset.column(self.column_name)
        return self._func(column_data)


CustomDescriptorCallable = Callable[[Dataset], Union[DatasetColumn, Dict[str, DatasetColumn]]]


class CustomDescriptor(Descriptor):
    func: str
    _func: Optional[CustomDescriptorCallable] = PrivateAttr(None)

    def __init__(self, func: Union[str, CustomDescriptorCallable], alias: Optional[str] = None):
        if callable(func):
            self._func = func
            self.func = f"{func.__module__}.{func.__name__}"
        else:
            self._func = None
            self.func = func
        super().__init__(alias=alias or f"custom_descriptor:{func.__name__}")

    def generate_data(self, dataset: "Dataset", options: Options) -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        if self._func is None:
            raise ValueError("CustomDescriptor is not configured with callable func")
        return self._func(dataset)
