import abc

from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
