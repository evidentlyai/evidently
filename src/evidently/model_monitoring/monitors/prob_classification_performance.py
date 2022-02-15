from evidently.analyzers import prob_classification_performance_analyzer
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class ProbClassificationPerformanceMonitorMetricsMonitor:
    _tag = 'prob_classification_performance'
    quality = ModelMonitoringMetric(f'{_tag}:quality', ['dataset', 'metric'])


class ProbClassificationPerformanceMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return 'prob_classification_performance'

    def analyzers(self):
        return [prob_classification_performance_analyzer.ProbClassificationPerformanceAnalyzer]

    @staticmethod
    def _yield_quality(
            metrics: prob_classification_performance_analyzer.ClassificationPerformanceMetrics,
            dataset: str,
    ):
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.accuracy, dict(dataset=dataset, metric='accuracy')
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.precision, dict(dataset=dataset, metric='precision')
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.recall, dict(dataset=dataset, metric='recall')
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.f1, dict(dataset=dataset, metric='f1')
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.roc_auc, dict(dataset=dataset, metric='roc_auc')
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.log_loss, dict(dataset=dataset, metric='log_loss')
        )

    def metrics(self, analyzer_results):
        results = prob_classification_performance_analyzer.ProbClassificationPerformanceAnalyzer.get_results(
            analyzer_results
        )

        for metric in self._yield_quality(results.reference_metrics, 'reference'):
            yield metric

        if results.current_metrics:
            for metric in self._yield_quality(results.current_metrics, 'current'):
                yield metric
