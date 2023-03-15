from typing import Generator

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceMetrics
from evidently.metric_results import DatasetColumns
from evidently.model_monitoring.monitoring import MetricsType
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class ProbClassificationPerformanceMonitorMetricsMonitor:
    """Class for probabilistic classification performance metrics in monitor.

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

    _tag = "prob_classification_performance"
    quality = ModelMonitoringMetric(f"{_tag}:quality", ["dataset", "metric"])
    class_representation = ModelMonitoringMetric(f"{_tag}:class_representation", ["dataset", "class_name", "type"])
    class_quality = ModelMonitoringMetric(f"{_tag}:class_quality", ["dataset", "class_name", "metric"])
    confusion = ModelMonitoringMetric(f"{_tag}:confusion", ["dataset", "class_x_name", "class_y_name"])
    class_confusion = ModelMonitoringMetric(f"{_tag}:class_confusion", ["dataset", "class_name", "metric"])


class ProbClassificationPerformanceMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "prob_classification_performance"

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    @staticmethod
    def _yield_metrics(
        metrics: ProbClassificationPerformanceMetrics,
        dataset: str,
        columns: DatasetColumns,
    ) -> Generator[MetricsType, None, None]:
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.accuracy, dict(dataset=dataset, metric="accuracy")
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.precision, dict(dataset=dataset, metric="precision")
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.recall, dict(dataset=dataset, metric="recall")
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.f1, dict(dataset=dataset, metric="f1")
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.roc_auc, dict(dataset=dataset, metric="roc_auc")
        )
        yield ProbClassificationPerformanceMonitorMetricsMonitor.quality.create(
            metrics.log_loss, dict(dataset=dataset, metric="log_loss")
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
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["precision"],
                dict(dataset=dataset, class_name=class_name, metric="precision"),
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["recall"],
                dict(dataset=dataset, class_name=class_name, metric="recall"),
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_quality.create(
                metrics.metrics_matrix[class_name]["f1-score"],
                dict(dataset=dataset, class_name=class_name, metric="f1"),
            )

        # process confusion metrics
        for idx, class_x_name in enumerate(metrics.confusion_matrix.labels):
            class_x_name = str(class_x_name)
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_representation.create(
                sum(metrics.confusion_matrix.values[idx]),
                dict(dataset=dataset, class_name=class_x_name, type="target"),
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_representation.create(
                sum([i[idx] for i in metrics.confusion_matrix.values]),
                dict(dataset=dataset, class_name=class_x_name, type="prediction"),
            )

            tp_value = metrics.confusion_by_classes[class_x_name]["tp"]
            fp_value = metrics.confusion_by_classes[class_x_name]["fp"]
            tn_value = metrics.confusion_by_classes[class_x_name]["tn"]
            fn_value = metrics.confusion_by_classes[class_x_name]["fn"]
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                tp_value, dict(dataset=dataset, class_name=class_x_name, metric="TP")
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                fp_value, dict(dataset=dataset, class_name=class_x_name, metric="FP")
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                tn_value, dict(dataset=dataset, class_name=class_x_name, metric="TN")
            )
            yield ProbClassificationPerformanceMonitorMetricsMonitor.class_confusion.create(
                fn_value, dict(dataset=dataset, class_name=class_x_name, metric="FN")
            )

            for idy, class_y_name in enumerate(metrics.confusion_matrix.labels):
                class_y_name = str(class_y_name)
                yield ProbClassificationPerformanceMonitorMetricsMonitor.confusion.create(
                    metrics.confusion_matrix.values[idx][idy],
                    dict(dataset=dataset, class_x_name=class_x_name, class_y_name=class_y_name),
                )

    def metrics(self, analyzer_results):
        results = ProbClassificationPerformanceAnalyzer.get_results(analyzer_results)

        for metric in self._yield_metrics(results.reference_metrics, "reference", columns=results.columns):
            yield metric

        if results.current_metrics:
            for metric in self._yield_metrics(results.current_metrics, "current", columns=results.columns):
                yield metric
