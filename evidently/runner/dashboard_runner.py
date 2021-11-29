from dataclasses import dataclass
from typing import Dict

from evidently.dashboard import Dashboard
from evidently.runner.runner import RunnerOptions, Runner
from evidently.tabs import DataDriftTab, CatTargetDriftTab, ClassificationPerformanceTab, \
    NumTargetDriftTab, ProbClassificationPerformanceTab, RegressionPerformanceTab
from evidently.tabs.base_tab import Verbose


@dataclass
class DashboardRunnerOptions(RunnerOptions):
    dashboard_tabs: Dict[str, Dict[str, str]]


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

        for tab, params in self.options.dashboard_tabs.items():
            tab_class = tabs_mapping.get(tab, None)
            if tab_class is None:
                raise ValueError(f"Unknown tab {tab}")
            verbose_level = params.get('verbose_level', None)
            tabs.append(tab_class(verbose_level=Verbose.parse_level(verbose_level)))

        dashboard = Dashboard(tabs=tabs)
        dashboard.calculate(reference_data, current_data, self.options.column_mapping)
        dashboard.save(self.options.output_path + ".html")
