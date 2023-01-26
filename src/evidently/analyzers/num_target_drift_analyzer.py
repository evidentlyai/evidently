from dataclasses import dataclass
from typing import Optional
from typing import Sequence

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.data_quality import get_rows_count
from evidently.options import DataDriftOptions
from evidently.utils.data_operations import process_columns


@dataclass
class NumTargetDriftAnalyzerResults(BaseAnalyzerResult):
    reference_data_count: int = 0
    current_data_count: int = 0
    target_metrics: Optional[ColumnDataDriftMetrics] = None
    prediction_metrics: Optional[ColumnDataDriftMetrics] = None


class NumTargetDriftAnalyzer(Analyzer):
    """Numerical target drift analyzer.

    Analyze numerical `target` and `prediction` distributions and provide calculations to the following questions:
    Does the model target behave similarly to the past period? Do my model predictions still look the same?

    For reference see https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift
    """

    @staticmethod
    def get_results(analyzer_results) -> NumTargetDriftAnalyzerResults:
        return analyzer_results[NumTargetDriftAnalyzer]

    def calculate(
        self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> NumTargetDriftAnalyzerResults:
        """Calculate the target and prediction drifts.

        With default options, uses a two sample Kolmogorov-Smirnov test at a 0.95 confidence level.

        Notes:
            You can also provide a custom function that computes a statistic by adding special
            `DataDriftOptions` object to the `option_provider` of the class.::

                options = DataDriftOptions(num_target_stattest_func=...)
                analyzer.options_prover.add(options)

            Such a function takes two arguments:::

                def(reference_data: pd.Series, current_data: pd.Series):
                   ...

            and returns arbitrary number (like a p_value from the other tests ;-))
        Args:
            reference_data: usually the data which you used in training.
            current_data: new, unseen data to which we compare the reference data.
            column_mapping: a `ColumnMapping` object that contains references to the name of target and prediction
                columns
        Returns:
            A dictionary that contains some meta information as well as `metrics` for either target or prediction
            columns or both. The `*_drift` column in `metrics` contains a computed p_value from tests.
        Raises:
            ValueError when target or predictions columns are not numerical.
        """
        if reference_data is None:
            raise ValueError("reference_data should be present")

        if current_data is None:
            raise ValueError("current_data should be present")

        if current_data is None:
            raise ValueError("current_data should be present")

        columns = process_columns(reference_data, column_mapping)
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        if not isinstance(target_column, str) and isinstance(columns.utility_columns.target, Sequence):
            raise ValueError("target should not be a sequence")

        if not isinstance(prediction_column, str) and isinstance(prediction_column, Sequence):
            raise ValueError("prediction should not be a sequence")

        if set(columns.num_feature_names) - set(current_data.columns):
            raise ValueError(
                f"Some numerical features in current data {current_data.columns}"
                f"are not present in columns.num_feature_names"
            )

        result = NumTargetDriftAnalyzerResults(
            columns=columns,
            reference_data_count=get_rows_count(reference_data),
            current_data_count=get_rows_count(current_data),
        )
        data_drift_options = self.options_provider.get(DataDriftOptions)

        if target_column is not None:
            result.target_metrics = get_one_column_drift(
                current_data=current_data,
                reference_data=reference_data,
                column_name=target_column,
                dataset_columns=columns,
                options=data_drift_options,
                column_type="num",
            )

        if prediction_column is not None:
            result.prediction_metrics = get_one_column_drift(
                current_data=current_data,
                reference_data=reference_data,
                column_name=prediction_column,
                dataset_columns=columns,
                options=data_drift_options,
                column_type="num",
            )

        return result
