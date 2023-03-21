import abc

from evidently.base_metric import InputData
from evidently.metric_results import DatasetColumns


class MetricPreset:
    """Base class for metric presets"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
