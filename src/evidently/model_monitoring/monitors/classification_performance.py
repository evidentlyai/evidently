import pandas as pd

from evidently.analyzers import classification_performance_analyzer
from evidently.model_monitoring import monitoring
from evidently.analyzers import utils


class ClassificationPerformanceMonitorMetricsMonitor:
    """Class for classification performance metrics.

     Metrics list:
         - quality: model quality with macro-average metrics in `reference` and `current` datasets
         Each metric name is marked as a `metric` label
         - class_representation: quantity of items in each class.
         A class name is marked as a `class_name` label
        - class_quality: quality metrics for each class
        - confusion: aggregated confusion metrics
     """
    _tag = 'classification_performance'
    quality = monitoring.ModelMonitoringMetric(f'{_tag}:quality', ['dataset', 'metric'])
    class_representation = monitoring.ModelMonitoringMetric(f'{_tag}:class_representation', ['dataset', 'class_name'])
    class_quality = monitoring.ModelMonitoringMetric(f'{_tag}:class_quality', ['dataset', 'class_name', 'metric'])
    confusion = monitoring.ModelMonitoringMetric(f'{_tag}:confusion', ['dataset', 'class_x_name', 'class_y_name'])


class ClassificationPerformanceMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'classification_performance'

    def analyzers(self):
        return [classification_performance_analyzer.ClassificationPerformanceAnalyzer]

    @staticmethod
    def _yield_metrics(
            metrics: classification_performance_analyzer.PerformanceMetrics,
            dataset: str,
            columns: utils.DatasetColumns,
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

        metrics_frame = pd.DataFrame(metrics.metrics_matrix)

        # try to move classes names to readable names via ColumnMapping settings
        if columns.target_names:
            classes_names = columns.target_names

        else:
            classes_names = metrics_frame.columns.tolist()[:-3]

        count_in_classes = metrics_frame.iloc[-1:, :-3].values[0]
        quality_by_classes = metrics_frame.iloc[:-1, :-3].T.values

        for idx, class_name in enumerate(classes_names):
            yield ClassificationPerformanceMonitorMetricsMonitor.class_representation.create(
                count_in_classes[idx], dict(dataset=dataset, class_name=class_name)
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                quality_by_classes[idx][0], dict(dataset=dataset, class_name=class_name, metric='precision')
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                quality_by_classes[idx][1], dict(dataset=dataset, class_name=class_name, metric='recall')
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                quality_by_classes[idx][2], dict(dataset=dataset, class_name=class_name, metric='f1')
            )

        # process confusion metrics
        for idx, class_x_name in enumerate(metrics.confusion_matrix.labels):
            for idy, class_y_name in enumerate(metrics.confusion_matrix.labels):
                yield ClassificationPerformanceMonitorMetricsMonitor.confusion.create(
                    metrics.confusion_matrix.values[idx][idy],
                    dict(dataset=dataset, class_x_name=class_x_name, class_y_name=class_y_name)
                )
        # TODO: move Confusion Matrix for classes with TP/FP/TN/FN to the analyzer, than add it here as metrics

    def metrics(self, analyzer_results):
        results = classification_performance_analyzer.ClassificationPerformanceAnalyzer.get_results(analyzer_results)

        for metric in self._yield_metrics(results.reference_metrics, 'reference', columns=results.columns):
            yield metric

        if results.current_metrics:
            for metric in self._yield_metrics(results.current_metrics, 'current', columns=results.columns):
                yield metric
