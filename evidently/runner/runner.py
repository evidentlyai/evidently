from typing import Optional, List, Dict

from dataclasses import dataclass

import pandas as pd


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
    column_mapping: Dict[str, str]
    output_path: str


class Runner:
    def __init__(self, options: RunnerOptions):
        self.options = options

    def _parse_data(self):
        ref_parse_dates = [self.options.reference_data_options.date_column] \
            if self.options.reference_data_options.date_column \
            else False
        reference_data = pd.read_csv(self.options.reference_data_path,
                                     header=0 if self.options.reference_data_options.header else None,
                                     sep=self.options.reference_data_options.separator,
                                     parse_dates=ref_parse_dates)

        if self.options.production_data_path:
            prod_parse_dates = [self.options.production_data_options.date_column] \
                if self.options.production_data_options.date_column \
                else False
            production_data = pd.read_csv(self.options.production_data_path,
                                          header=0 if self.options.production_data_options.header else None,
                                          sep=self.options.production_data_options.separator,
                                          parse_dates=prod_parse_dates)
        else:
            production_data = None

        return reference_data, production_data
