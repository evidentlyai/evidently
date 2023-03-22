import abc

from evidently.base_metric import InputData
from evidently.metric_results import DatasetColumns


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
