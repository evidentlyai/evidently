import abc

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
