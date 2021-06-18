from dataclasses import dataclass
from typing import List

from evidently.dashboard import Dashboard
from evidently.runner.runner import RunnerOptions, Runner
from evidently.tabs import DataDriftTab, CatTargetDriftTab, ClassificationPerformanceTab, \
    NumTargetDriftTab, ProbClassificationPerformanceTab, RegressionPerformanceTab


@dataclass
class DashboardRunnerOptions(RunnerOptions):
    dashboard_tabs: List[str]


tabs_mapping = dict(
    data_drift=DataDriftTab,
    cat_target_drift=CatTargetDriftTab,
    classification_performance=ClassificationPerformanceTab,
    prob_classification_performance=ProbClassificationPerformanceTab,
    num_target_drift=NumTargetDriftTab,
    regression_performance=RegressionPerformanceTab,
)


class DashboardRunner(Runner):
    def __init__(self, options: DashboardRunnerOptions):
        super().__init__(options)
        self.options = options

    def run(self):
        (reference_data, current_data) = self._parse_data()

        tabs = []

        for tab in self.options.dashboard_tabs:
            tab_class = tabs_mapping.get(tab, None)
            if tab_class is None:
                raise ValueError(f"Unknown tab {tab}")
            tabs.append(tab_class)

        dashboard = Dashboard(tabs=tabs)
        dashboard.calculate(reference_data, current_data, self.options.column_mapping)
        dashboard.save(self.options.output_path + ".html")
