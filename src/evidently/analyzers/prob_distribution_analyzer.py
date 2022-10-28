from typing import Optional

import dataclasses
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ProbDistributionAnalyzerResults(BaseAnalyzerResult):
    pass


# TODO: Move logic from `evidently.dashboard.widgets.prob_class_pred_distr_widget.py` to here
class ProbDistributionAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> ProbDistributionAnalyzerResults:
        return analyzer_results[ProbDistributionAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
    ) -> ProbDistributionAnalyzerResults:
        columns = process_columns(reference_data, column_mapping)

        return ProbDistributionAnalyzerResults(columns=columns)
