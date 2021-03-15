from typing import Optional, List

import pandas as pd
from dataclasses import dataclass

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab


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
    output_path: str


class Runner:
    def __init__(self, options: RunnerOptions):
        self.options = options

    def run(self):
        reference_data = pd.read_csv(self.options.reference_data_path,
                                     header=0 if self.options.reference_data_options.header else None,
                                     sep=self.options.reference_data_options.separator,
                                     parse_dates=[self.options.reference_data_options.date_column],
                                     index_col=self.options.reference_data_options.date_column)

        if self.options.production_data_path:
            production_data = pd.read_csv(self.options.production_data_path,
                                          header=0 if self.options.production_data_options.header else None,
                                          sep=self.options.production_data_options.separator,
                                          parse_dates=[self.options.production_data_options.date_column],
                                          index_col=self.options.production_data_options.date_column)
        else:
            production_data = None
        report = Dashboard(reference_data, production_data, tabs=[DriftTab])
        report.save(self.options.output_path)
