import abc

from evidently.utils.data_preprocessing import DataDefinition


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data_definition: DataDefinition):
        raise NotImplementedError()
