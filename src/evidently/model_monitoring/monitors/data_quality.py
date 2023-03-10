from typing import Generator

import pandas as pd

from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.calculations.data_quality import DataQualityStats
from evidently.model_monitoring.monitoring import MetricsType
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class DataQualityMonitorMetrics:
    _tag = "data_quality"
    quality_stat = ModelMonitoringMetric(
        f"{_tag}:quality_stat", ["dataset", "feature", "feature_type", "metric"]
    )


class DataQualityMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "data_quality"

    def analyzers(self):
        return [DataQualityAnalyzer]

    @staticmethod
    def _yield_metrics(
        data_stats: DataQualityStats,
        dataset: str,
    ) -> Generator[MetricsType, None, None]:
        for feature_name, feature_stats in data_stats.get_all_features().items():
            feature_stats_dict = feature_stats.as_dict()
            feature_type = feature_stats_dict.pop("feature_type")
            for stat_name, stat_value in feature_stats_dict.items():
                if stat_value is not None:
                    if pd.isnull(stat_value):
                        stat_value = None

                    yield DataQualityMonitorMetrics.quality_stat.create(
                        stat_value,
                        {
                            "dataset": dataset,
                            "feature": feature_name,
                            "feature_type": feature_type,
                            "metric": stat_name,
                        },
                    )

    def metrics(self, analyzer_results) -> Generator[MetricsType, None, None]:
        results = DataQualityAnalyzer.get_results(analyzer_results)

        if results.reference_features_stats is not None:
            for metric in self._yield_metrics(
                results.reference_features_stats, "reference"
            ):
                yield metric

        if results.current_features_stats is not None:
            for metric in self._yield_metrics(
                results.current_features_stats, "current"
            ):
                yield metric
