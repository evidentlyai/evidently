import abc

from evidently.utils.data_preprocessing import DataDefinition


class MetricPreset:
    """Base class for metric presets"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_metrics(self, data_definition: DataDefinition):
        raise NotImplementedError()
