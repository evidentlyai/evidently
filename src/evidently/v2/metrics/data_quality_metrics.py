from typing import Dict
from typing import Optional

import pandas as pd
from dataclasses import dataclass

from evidently.analyzers.data_quality_analyzer import DataQualityStats
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.utils import process_columns
from evidently.options.quality_metrics import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class DataQualityMetricsResults:
    features_stats: DataQualityStats
    reference_correlations: Dict[str, pd.DataFrame]


class DataQualityMetrics(Metric[DataQualityMetricsResults]):
    def __init__(self, options: QualityMetricsOptions = None) -> None:
        self.analyzer = DataQualityAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataQualityMetricsResults:
        if data.current_data is None:
            raise ValueError("current_data should be present")

        elif data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data,
                current_data=None,
                column_mapping=data.column_mapping
            )
            results = DataQualityMetricsResults(
                features_stats=analyzer_results.reference_features_stats,
                reference_correlations=analyzer_results.reference_correlations
            )

        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data,
                current_data=data.current_data,
                column_mapping=data.column_mapping
            )
            results = DataQualityMetricsResults(
                features_stats=analyzer_results.current_features_stats,
                reference_correlations=analyzer_results.current_correlations
            )
        return results


@dataclass
class DataStabilityMetricsResults:
    # quantity of not-stable target values. None value if there is no target in the dataset.
    target_not_stable: Optional[int] = None
    # quantity of not-stable prediction values. None value if there is no target in the dataset.
    prediction_not_stable: Optional[int] = None


class DataStabilityMetrics(Metric[DataStabilityMetricsResults]):
    """
    Calculates stability of target and prediction by features values

    If we have the same features values, but different target/prediction value - the value is not stable
    """
    def __init__(self, options: QualityMetricsOptions = None) -> None:
        self.analyzer = DataQualityAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataStabilityMetricsResults:
        if data.current_data is None:
            raise ValueError("current_data should be present")

        columns = process_columns(data.current_data, data.column_mapping)
        target_name = columns.utility_columns.target
        prediction_name = columns.utility_columns.prediction

        if target_name in data.current_data:
            target_not_stable_count = 0

        else:
            target_not_stable_count = None

        if prediction_name in data.current_data:
            prediction_not_stable_count = 0

        else:
            prediction_not_stable_count = None

        if target_not_stable_count is None and prediction_not_stable_count is None:
            return DataStabilityMetricsResults()

        target_cache = {}
        prediction_cache = {}

        for _, row in data.current_data.iterrows():
            if target_not_stable_count is not None:
                target_value = row[target_name]

                if target_value in target_cache:
                    # temporary not calculate stability by all features, need to specify requirements
                    target_not_stable_count += 1

                else:
                    target_cache[target_value] = row

            if prediction_not_stable_count is not None:
                prediction_value = row[prediction_name]

                if prediction_value in prediction_cache:
                    # temporary not calculate stability by all features, need to specify requirements
                    prediction_not_stable_count += 1

                else:
                    prediction_cache[prediction_value] = row

        return DataStabilityMetricsResults(
            target_not_stable=target_not_stable_count,
            prediction_not_stable=prediction_not_stable_count
        )
