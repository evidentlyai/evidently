from typing import Dict
from typing import Optional

import pandas as pd
from dataclasses import dataclass

from evidently.analyzers.data_quality_analyzer import DataQualityStats
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.options.quality_metrics import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class DataQualityMetricsResults:
    features_stats: DataQualityStats
    target_prediction_correlation: Optional[float]
    correlations: Dict[str, pd.DataFrame] = None
    reference_features_stats: Optional[DataQualityStats] = None


class DataQualityMetrics(Metric[DataQualityMetricsResults]):
    def __init__(self, options: QualityMetricsOptions = None) -> None:
        self.analyzer = DataQualityAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataQualityMetricsResults:
        if data.current_data is None:
            raise ValueError("Current dataset should be present")

        if data.column_mapping.target and data.column_mapping.prediction and \
                data.column_mapping.target in data.current_data and \
                data.column_mapping.prediction in data.current_data:
            target_prediction_correlation = data.current_data[data.column_mapping.target].corr(
                data.current_data[data.column_mapping.prediction]
            )

        else:
            target_prediction_correlation = None

        if data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data,
                current_data=None,
                column_mapping=data.column_mapping
            )
            features_stats = analyzer_results.reference_features_stats
            correlations = analyzer_results.reference_correlations
            reference_features_stats = None

        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data,
                current_data=data.current_data,
                column_mapping=data.column_mapping
            )
            features_stats = analyzer_results.current_features_stats
            correlations = analyzer_results.current_correlations
            reference_features_stats = analyzer_results.reference_features_stats

        return DataQualityMetricsResults(
            target_prediction_correlation=target_prediction_correlation,
            features_stats=features_stats,
            correlations=correlations,
            reference_features_stats=reference_features_stats
        )


@dataclass
class DataQualityStabilityMetricsResults:
    number_not_stable_target: Optional[int] = None
    number_not_stable_prediction: Optional[int] = None


class DataQualityStabilityMetrics(Metric[DataQualityStabilityMetricsResults]):
    """Calculates stability by target and prediction"""

    def calculate(self, data: InputData, metrics: dict) -> DataQualityStabilityMetricsResults:
        result = DataQualityStabilityMetricsResults()
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        columns = [column for column in data.current_data.columns if column not in (target_name, prediction_name)]
        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]

        if target_name in data.current_data:
            result.number_not_stable_target = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]

        if prediction_name in data.current_data:
            result.number_not_stable_prediction = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [prediction_name], keep=False)].index
            ).shape[0]

        return result
