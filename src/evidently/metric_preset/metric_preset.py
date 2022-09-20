import abc

from evidently.metrics.base_metric import InputData
from evidently.utils.data_operations import DatasetColumns


class MetricPreset:
    """Base class for metric presets"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
