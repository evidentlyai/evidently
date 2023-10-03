import abc

from evidently.base_metric import InputData
from evidently.metric_results import DatasetColumns
from evidently.utils.data_preprocessing import DataDefinition


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data_definition: DataDefinition):
        raise NotImplementedError()
