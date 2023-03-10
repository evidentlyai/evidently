from dataclasses import dataclass
from typing import Dict

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import CatTargetDriftTab
from evidently.dashboard.tabs import ClassificationPerformanceTab
from evidently.dashboard.tabs import DataDriftTab
from evidently.dashboard.tabs import DataQualityTab
from evidently.dashboard.tabs import NumTargetDriftTab
from evidently.dashboard.tabs import ProbClassificationPerformanceTab
from evidently.dashboard.tabs import RegressionPerformanceTab
from evidently.runner.runner import Runner
from evidently.runner.runner import RunnerOptions


@dataclass
class DashboardRunnerOptions(RunnerOptions):
    dashboard_tabs: Dict[str, Dict[str, object]]


tabs_mapping = dict(
    data_drift=DataDriftTab,
    cat_target_drift=CatTargetDriftTab,
    classification_performance=ClassificationPerformanceTab,
    prob_classification_performance=ProbClassificationPerformanceTab,
    num_target_drift=NumTargetDriftTab,
    regression_performance=RegressionPerformanceTab,
    data_quality=DataQualityTab,
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
            try:
                verbose_level = (
                    int(params.get("verbose_level", None)) if params.get("verbose_level", None) is not None else None
                )
            except ValueError as ex:
                raise ValueError(f"Failed to parse verbose level for tab {tab}") from ex
            include_widgets = params.get("include_widgets", None)
            tabs.append(tab_class(verbose_level=verbose_level, include_widgets=include_widgets))

        dashboard = Dashboard(tabs=tabs, options=self.options.options)
        dashboard.calculate(reference_data, current_data, self.options.column_mapping)
        dashboard.save(self.options.output_path + ".html")
