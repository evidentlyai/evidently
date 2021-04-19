import pandas

from evidently.dashboard import Dashboard


class Pipeline:
    def __init__(self, dashboard: Dashboard):
        self.dashboard = dashboard
        self.analyzes_results = dict()

    def execute(self,
                reference_data: pandas.DataFrame,
                production_data: pandas.DataFrame,
                column_mapping: dict = None):
        analyzes = self.dashboard.analyzes
        for analyze in analyzes:
            self.analyzes_results[analyze] = analyze().calculate(reference_data, production_data, column_mapping)
        self.dashboard.calculate(reference_data, production_data, column_mapping, self.analyzes_results)
