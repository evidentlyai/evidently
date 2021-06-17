import logging
from typing import Optional, List, Dict

from dataclasses import dataclass

from evidently.runner.loader import DataLoader, SamplingOptions, DataOptions


@dataclass
class RunnerOptions:
    reference_data_path: str
    reference_data_options: DataOptions
    reference_data_sampling: Optional[SamplingOptions]
    current_data_path: Optional[str]
    current_data_options: Optional[DataOptions]
    current_data_sampling: Optional[SamplingOptions]
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
        if self.options.current_data_path:
            current_data = loader.load(self.options.current_data_path,
                                          self.options.current_data_options,
                                          self.options.current_data_sampling)
            logging.info(f"current dataset loaded: {len(current_data)} rows")
        else:
            current_data = None

        return reference_data, current_data
