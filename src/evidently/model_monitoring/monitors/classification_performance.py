from typing import Generator

import evidently.metric_results
import evidently.utils.data_operations
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceMetrics
from evidently.model_monitoring.monitoring import MetricsType
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class ClassificationPerformanceMonitorMetricsMonitor:
    """Class for classification performance metrics in monitor.

    Metrics list:

        - quality: model quality with macro-average metrics in `reference` and `current` datasets
            Each metric name is marked as a `metric` label
        - class_representation: quantity of items in each class
            A class name is marked as a `class_name` label
        `target` and `prediction` columns are marked as `type`
        - class_quality: quality metrics for each class
        - confusion: aggregated confusion metrics
        - class_confusion: confusion (TP, TN, FP, FN) by class

    """

    _tag = "classification_performance"
    quality = ModelMonitoringMetric(f"{_tag}:quality", ["dataset", "metric"])
    class_representation = ModelMonitoringMetric(f"{_tag}:class_representation", ["dataset", "class_name", "type"])
    class_quality = ModelMonitoringMetric(f"{_tag}:class_quality", ["dataset", "class_name", "metric"])
    confusion = ModelMonitoringMetric(f"{_tag}:confusion", ["dataset", "class_x_name", "class_y_name"])
    class_confusion = ModelMonitoringMetric(f"{_tag}:class_confusion", ["dataset", "class_name", "metric"])


class ClassificationPerformanceMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "classification_performance"

    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    @staticmethod
    def _yield_metrics(
        metrics: ClassificationPerformanceMetrics,
        dataset: str,
        columns: evidently.metric_results.DatasetColumns,
    ) -> Generator[MetricsType, None, None]:
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.accuracy, dict(dataset=dataset, metric="accuracy")
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.precision, dict(dataset=dataset, metric="precision")
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.recall, dict(dataset=dataset, metric="recall")
        )
        yield ClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.f1, dict(dataset=dataset, metric="f1")
        )

        # try to move classes names to readable names via ColumnMapping settings
        classes_names = columns.target_names_list
        if classes_names is None:
            # get classes list from the matrix data
            # remove the last 3 key - it is avg metrix values 'accuracy', 'macro avg', 'weighted avg'
            classes_names = [
                key for key in metrics.metrics_matrix.keys() if key not in ("accuracy", "macro avg", "weighted avg")
            ]

        for class_name in classes_names:
            class_name = str(class_name)
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["precision"],
                dict(dataset=dataset, class_name=class_name, metric="precision"),
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["recall"],
                dict(dataset=dataset, class_name=class_name, metric="recall"),
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["f1-score"],
                dict(dataset=dataset, class_name=class_name, metric="f1"),
            )

        # process confusion metrics
        for idx, class_x_name in enumerate(metrics.confusion_matrix.labels):
            class_x_name_str = str(class_x_name)
            # todo better typing?
            assert isinstance(class_x_name, (int, str))
            yield ClassificationPerformanceMonitorMetricsMonitor.class_representation.create(
                sum(metrics.confusion_matrix.values[idx]),
                dict(dataset=dataset, class_name=class_x_name_str, type="target"),
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_representation.create(
                sum([i[idx] for i in metrics.confusion_matrix.values]),
                dict(dataset=dataset, class_name=class_x_name_str, type="prediction"),
            )

            tp_value = metrics.confusion_by_classes[class_x_name]["tp"]
            fp_value = metrics.confusion_by_classes[class_x_name]["fp"]
            tn_value = metrics.confusion_by_classes[class_x_name]["tn"]
            fn_value = metrics.confusion_by_classes[class_x_name]["fn"]
            yield ClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                tp_value, dict(dataset=dataset, class_name=class_x_name_str, metric="TP")
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                fp_value, dict(dataset=dataset, class_name=class_x_name_str, metric="FP")
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                tn_value, dict(dataset=dataset, class_name=class_x_name_str, metric="TN")
            )
            yield ClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                fn_value, dict(dataset=dataset, class_name=class_x_name_str, metric="FN")
            )

            for idy, class_y_name in enumerate(metrics.confusion_matrix.labels):
                class_y_name = str(class_y_name)
                yield ClassificationPerformanceMonitorMetricsMonitor.confusion.create(
                    metrics.confusion_matrix.values[idx][idy],
                    dict(dataset=dataset, class_x_name=class_x_name_str, class_y_name=class_y_name),
                )

    def metrics(self, analyzer_results) -> Generator[MetricsType, None, None]:
        results = ClassificationPerformanceAnalyzer.get_results(analyzer_results)

        if results.reference_metrics is not None:
            for metric in self._yield_metrics(results.reference_metrics, "reference", columns=results.columns):
                yield metric

        if results.current_metrics is not None:
            for metric in self._yield_metrics(results.current_metrics, "current", columns=results.columns):
                yield metric
