import abc
import pandas


class Pipeline:
    def __init__(self):
        self.analyzers_results = dict()

    @abc.abstractmethod
    def get_analyzers(self):
        raise NotImplementedError("get_analyzers should be implemented")

    def execute(self,
                reference_data: pandas.DataFrame,
                production_data: pandas.DataFrame,
                column_mapping: dict = None):
        for analyzer in self.get_analyzers():
            self.analyzers_results[analyzer] = analyzer().calculate(reference_data, production_data, column_mapping)
