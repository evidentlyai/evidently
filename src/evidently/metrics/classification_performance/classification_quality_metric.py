from typing import List
from typing import Optional
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from sklearn import metrics

from evidently import ColumnMapping
from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.calculations.classification_performance import calculate_confusion_by_classes
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class DatasetClassificationQuality:
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None


@dataclasses.dataclass
class ClassificationQualityMetricResult:
    current: DatasetClassificationQuality
    reference: Optional[DatasetClassificationQuality]
    target_name: str


class ClassificationQualityMetric(ThresholdClassificationMetric[ClassificationQualityMetricResult]):
    confusion_matrix_metric: ClassificationConfusionMatrix

    def __init__(
        self,
        threshold: Optional[float] = None,
        k: Optional[Union[float, int]] = None,
        # average: str = "macro",
    ):
        super().__init__(threshold, k)
        # self.average = average
        self.confusion_matrix_metric = ClassificationConfusionMatrix(threshold, k)

    def calculate(self, data: InputData) -> ClassificationQualityMetricResult:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        current = self.calculate_metrics(
            data.current_data,
            data.column_mapping,
            self.confusion_matrix_metric.get_result().current_matrix,
        )
        reference = None
        if data.reference_data is not None:
            ref_matrix = self.confusion_matrix_metric.get_result().reference_matrix
            if ref_matrix is None:
                raise ValueError(f"Dependency {self.confusion_matrix_metric.__class__} should have reference data")
            reference = self.calculate_metrics(
                data.reference_data,
                data.column_mapping,
                ref_matrix,
            )
        return ClassificationQualityMetricResult(current=current, reference=reference, target_name=target_name)

    def calculate_metrics(
        self,
        data: pd.DataFrame,
        column_mapping: ColumnMapping,
        confusion_matrix: ConfusionMatrix,
    ) -> DatasetClassificationQuality:
        target, prediction = self.get_target_prediction_data(data, column_mapping)
        if column_mapping.pos_label is not None:
            pos_label = column_mapping.pos_label
        else:
            pos_label = 1
        tpr = None
        tnr = None
        fpr = None
        fnr = None
        roc_auc = None
        log_loss = None
        if len(prediction.labels) == 2:
            confusion_by_classes = calculate_confusion_by_classes(
                np.array(confusion_matrix.values),
                confusion_matrix.labels,
            )
            conf_by_pos_label = confusion_by_classes[confusion_matrix.labels[0]]
            precision = metrics.precision_score(target, prediction.predictions, pos_label=pos_label)
            recall = metrics.recall_score(target, prediction.predictions, pos_label=pos_label)
            f1 = metrics.f1_score(target, prediction.predictions, pos_label=pos_label)
            tpr = conf_by_pos_label["tp"] / (conf_by_pos_label["tp"] + conf_by_pos_label["fn"])
            tnr = conf_by_pos_label["tn"] / (conf_by_pos_label["tn"] + conf_by_pos_label["fp"])
            fpr = conf_by_pos_label["fp"] / (conf_by_pos_label["fp"] + conf_by_pos_label["tn"])
            fnr = conf_by_pos_label["fn"] / (conf_by_pos_label["fn"] + conf_by_pos_label["tp"])
        else:
            precision = metrics.precision_score(target, prediction.predictions, average="macro")
            recall = metrics.recall_score(target, prediction.predictions, average="macro")
            f1 = metrics.f1_score(target, prediction.predictions, average="macro")
        if prediction.prediction_probas is not None:
            binaraized_target = (
                target.astype(str).values.reshape(-1, 1) == list(prediction.prediction_probas.columns.astype(str))
            ).astype(int)
            prediction_probas_array = prediction.prediction_probas.to_numpy()
            roc_auc = metrics.roc_auc_score(binaraized_target, prediction_probas_array, average="macro")
            log_loss = metrics.log_loss(binaraized_target, prediction_probas_array)

        return DatasetClassificationQuality(
            accuracy=metrics.accuracy_score(target, prediction.predictions),
            precision=precision,
            recall=recall,
            f1=f1,
            tpr=tpr,
            tnr=tnr,
            fpr=fpr,
            fnr=fnr,
            roc_auc=roc_auc,
            log_loss=log_loss,
        )


@default_renderer(wrap_type=ClassificationQualityMetric)
class ClassificationQualityMetricRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationQualityMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        return result

    def render_html(self, obj: ClassificationQualityMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        target_name = metric_result.target_name
        result = []
        counters = [
            CounterData("Accuracy", f"{round(metric_result.current.accuracy, 3)}"),
            CounterData("Precision", f"{round(metric_result.current.precision, 3)}"),
            CounterData("Recall", f"{round(metric_result.current.recall, 3)}"),
            CounterData("F1", f"{round(metric_result.current.f1, 3)}"),
        ]
        if metric_result.current.roc_auc is not None and metric_result.current.log_loss is not None:
            counters.extend(
                [
                    CounterData("ROC AUC", f"{round(metric_result.current.roc_auc, 3)}"),
                    CounterData("LogLoss", f"{round(metric_result.current.log_loss, 3)}"),
                ]
            )
        result.append(header_text(label=f"Classification Model Performance. Target: '{target_name}’"))
        result.append(counter(title="Current: Model Quality Metrics", counters=counters))

        if metric_result.reference is not None:
            counters = [
                CounterData("Accuracy", f"{round(metric_result.reference.accuracy, 3)}"),
                CounterData("Precision", f"{round(metric_result.reference.precision, 3)}"),
                CounterData("Recall", f"{round(metric_result.reference.recall, 3)}"),
                CounterData("F1", f"{round(metric_result.reference.f1, 3)}"),
            ]
            if metric_result.reference.roc_auc is not None and metric_result.reference.log_loss is not None:
                counters.extend(
                    [
                        CounterData("ROC AUC", f"{round(metric_result.reference.roc_auc, 3)}"),
                        CounterData("LogLoss", f"{round(metric_result.reference.log_loss, 3)}"),
                    ]
                )
            result.append(counter(title="Reference: Model Quality Metrics", counters=counters))
        return result
