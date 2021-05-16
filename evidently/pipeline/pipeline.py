import abc
import pandas


class Pipeline:
    def __init__(self):
        self.analyzes_results = dict()

    @abc.abstractmethod
    def get_analyzes(self):
        raise NotImplementedError("get_analyzes should be implemented")

    def execute(self,
                reference_data: pandas.DataFrame,
                production_data: pandas.DataFrame,
                column_mapping: dict = None):
        for analyze in self.get_analyzes():
            self.analyzes_results[analyze] = analyze().calculate(reference_data, production_data, column_mapping)
