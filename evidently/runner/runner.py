from typing import Optional, List, Dict

import pandas as pd
from dataclasses import dataclass

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab, CatTargetDriftTab, ClassificationPerformanceTab,\
    NumTargetDriftTab, ProbClassificationPerformanceTab, RegressionPerformanceTab


class DataOptions:
    date_column: str
    separator: str
    # is csv file contains header row
    header: bool
    # should be list of names, or None if columns should be inferred from data
    column_names: Optional[List[str]]

    def __init__(self, date_column: str = "datetime", separator=",", header=True, column_names=None):
        self.date_column = date_column
        self.header = header
        self.separator = separator
        self.column_names = column_names


@dataclass
class RunnerOptions:
    reference_data_path: str
    reference_data_options: DataOptions
    production_data_path: Optional[str]
    production_data_options: Optional[DataOptions]
    dashboard_tabs: List[str]
    column_mapping: Dict[str, str]
    output_path: str


tabs_mapping = dict(
    drift=DriftTab,
    cat_target_drift=CatTargetDriftTab,
    classification_performance=ClassificationPerformanceTab,
    prob_classification_performance=ProbClassificationPerformanceTab,
    num_target_drift=NumTargetDriftTab,
    regression_performance=RegressionPerformanceTab,
)


class Runner:
    def __init__(self, options: RunnerOptions):
        self.options = options

    def run(self):
        reference_data = pd.read_csv(self.options.reference_data_path,
                                     header=0 if self.options.reference_data_options.header else None,
                                     sep=self.options.reference_data_options.separator,
                                     parse_dates=[self.options.reference_data_options.date_column] if self.options.reference_data_options.date_column else False)
                                     #index_col=self.options.reference_data_options.date_column)

        if self.options.production_data_path:
            production_data = pd.read_csv(self.options.production_data_path,
                                          header=0 if self.options.production_data_options.header else None,
                                          sep=self.options.production_data_options.separator,
                                          parse_dates=[self.options.production_data_options.date_column] if self.options.production_data_options.date_column else False)
                                          #index_col=self.options.production_data_options.date_column)
        else:
            production_data = None

        tabs = []

        for tab in self.options.dashboard_tabs:
            tab_class = tabs_mapping.get(tab, None)
            if tab_class is None:
                raise ValueError(f"Unknown tab {tab}")
            tabs.append(tab_class)

        report = Dashboard(reference_data, production_data, tabs=tabs, column_mapping=self.options.column_mapping)
        report.save(self.options.output_path)
