import logging
from typing import Optional, List, Dict

from dataclasses import dataclass

from evidently.runner.loader import DataLoader, SamplingOptions, DataOptions


@dataclass
class RunnerOptions:
    reference_data_path: str
    reference_data_options: DataOptions
    reference_data_sampling: Optional[SamplingOptions]
    production_data_path: Optional[str]
    production_data_options: Optional[DataOptions]
    production_data_sampling: Optional[SamplingOptions]
    column_mapping: Dict[str, str]
    output_path: str


class Runner:
    def __init__(self, options: RunnerOptions):
        self.options = options

    def _parse_data(self):
        loader = DataLoader()

        reference_data = loader.load(self.options.reference_data_path,
                                     self.options.reference_data_options,
                                     self.options.reference_data_sampling)
        logging.info(f"reference dataset loaded: {len(reference_data)} rows")
        if self.options.production_data_path:
            production_data = loader.load(self.options.production_data_path,
                                          self.options.production_data_options,
                                          self.options.production_data_sampling)
            logging.info(f"production dataset loaded: {len(production_data)} rows")
        else:
            production_data = None

        return reference_data, production_data
