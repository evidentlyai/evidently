import abc

from evidently.utils.data_operations import DatasetColumns
from evidently.metrics.base_metric import InputData


class MetricPreset:
    """Base class for metric presets"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
