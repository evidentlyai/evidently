#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd
from dataclasses import dataclass

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.calculations.data_drift import DatasetDriftMetrics
from evidently.calculations.data_drift import get_drift_for_columns
from evidently.options import DataDriftOptions
from evidently.utils.data_operations import process_columns


@dataclass
class DataDriftAnalyzerResults(BaseAnalyzerResult):
    options: DataDriftOptions
    metrics: DatasetDriftMetrics


class DataDriftAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> DataDriftAnalyzerResults:
        return analyzer_results[DataDriftAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
    ) -> DataDriftAnalyzerResults:
        if current_data is None:
            raise ValueError("current_data should be present")

        data_drift_options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result_metrics = get_drift_for_columns(
            current_data=current_data,
            reference_data=reference_data,
            dataset_columns=columns,
            data_drift_options=data_drift_options,
        )

        result = DataDriftAnalyzerResults(
            columns=columns,
            options=data_drift_options,
            metrics=result_metrics,
        )
        return result
