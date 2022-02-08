from evidently.analyzers import classification_performance_analyzer
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class ClassificationPerformanceMonitorMetricsMonitor:
    _tag = 'classification_performance'
    quality = ModelMonitoringMetric(f'{_tag}:quality', ['dataset', 'metric'])


class ClassificationPerformanceMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "classification_performance"

    def analyzers(self):
        return [classification_performance_analyzer.ClassificationPerformanceAnalyzer]

    @staticmethod
    def _yield_quality(
            metrics: classification_performance_analyzer.PerformanceMetrics,
            dataset: str,
    ):
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.accuracy, dict(dataset=dataset, metric='accuracy')
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.precision, dict(dataset=dataset, metric='precision')
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.recall, dict(dataset=dataset, metric='recall')
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.f1, dict(dataset=dataset, metric='f1')
        )

    def metrics(self, analyzer_results):
        results = classification_performance_analyzer.ClassificationPerformanceAnalyzer.get_results(analyzer_results)

        for metric in self._yield_quality(results.reference_metrics, 'reference'):
            yield metric

        if results.current_metrics:
            for metric in self._yield_quality(results.current_metrics, 'current'):
                yield metric
