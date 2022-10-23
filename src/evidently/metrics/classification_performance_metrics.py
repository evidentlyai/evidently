import abc
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
import sklearn

from evidently import ColumnMapping
from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.calculations.classification_performance import calculate_confusion_by_classes
from evidently.calculations.classification_performance import get_prediction_data
from evidently.calculations.classification_performance import k_probability_threshold
from evidently.calculations.classification_performance import threshold_probability_labels
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class DatasetClassificationPerformanceMetrics:
    """Class for performance metrics values"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    metrics_matrix: dict
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[Union[str, int], Dict[str, int]]
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    roc_aucs: Optional[list] = None
    roc_curve: Optional[dict] = None
    pr_curve: Optional[dict] = None
    pr_table: Optional[Union[dict, list]] = None
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[dict] = None
    plot_data: Optional[Dict[str, Dict[str, list]]] = None


@dataclasses.dataclass
class ClassificationPerformanceResults:
    columns: DatasetColumns
    current: DatasetClassificationPerformanceMetrics
    dummy: DatasetClassificationPerformanceMetrics
    reference: Optional[DatasetClassificationPerformanceMetrics] = None


def _calculate_k_variant(
    target_data: pd.Series, prediction_probas: pd.DataFrame, labels: List[str], k: Union[int, float]
):
    if prediction_probas is None or len(labels) > 2:
        raise ValueError("Top K parameter can be used only with binary classification with probas")

    pos_label, neg_label = prediction_probas.columns
    prediction_labels = threshold_probability_labels(
        prediction_probas, pos_label, neg_label, k_probability_threshold(prediction_probas, k)
    )
    return classification_performance_metrics(target_data, prediction_labels, prediction_probas, pos_label)


def _calculate_threshold(target_data: pd.Series, prediction_probas: pd.DataFrame, threshold: float):
    pos_label, neg_label = prediction_probas.columns
    prediction_labels = threshold_probability_labels(prediction_probas, pos_label, neg_label, threshold)
    return classification_performance_metrics(target_data, prediction_labels, prediction_probas, pos_label)


def classification_performance_metrics(
    target: pd.Series,
    prediction: pd.Series,
    prediction_probas: Optional[pd.DataFrame],
    pos_label: Optional[Union[str, int]],
) -> DatasetClassificationPerformanceMetrics:

    class_num = target.nunique()
    prediction_labels = prediction

    if class_num > 2:
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(target, prediction_labels, average="macro")
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="macro")
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="macro")

    else:
        accuracy_score = sklearn.metrics.accuracy_score(target, prediction_labels)
        avg_precision = sklearn.metrics.precision_score(
            target, prediction_labels, average="binary", pos_label=pos_label
        )
        avg_recall = sklearn.metrics.recall_score(target, prediction_labels, average="binary", pos_label=pos_label)
        avg_f1 = sklearn.metrics.f1_score(target, prediction_labels, average="binary", pos_label=pos_label)

    roc_auc: Optional[float] = None
    roc_aucs: Optional[list] = None
    log_loss: Optional[float] = None
    roc_curve: Optional[dict] = None

    if prediction_probas is not None:
        binaraized_target = (
            target.astype(str).values.reshape(-1, 1) == list(prediction_probas.columns.astype(str))
        ).astype(int)
        array_prediction = prediction_probas.to_numpy()
        roc_auc = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average="macro")
        log_loss = sklearn.metrics.log_loss(binaraized_target, array_prediction)
        roc_aucs = sklearn.metrics.roc_auc_score(binaraized_target, array_prediction, average=None).tolist()  # noqa
        # roc curve
        roc_curve = {}
        binaraized_target = pd.DataFrame(binaraized_target)
        binaraized_target.columns = list(prediction_probas.columns)
        for label in binaraized_target.columns:
            fprs, tprs, thrs = sklearn.metrics.roc_curve(binaraized_target[label], prediction_probas[label])
            roc_curve[label] = {"fpr": fprs.tolist(), "tpr": tprs.tolist(), "thrs": thrs.tolist()}

    # calculate class support and metrics matrix
    metrics_matrix = sklearn.metrics.classification_report(target, prediction_labels, output_dict=True)

    # calculate confusion matrix
    # labels = target_names if target_names else sorted(set(target.unique()) | set(prediction.unique()))
    labels = sorted(set(target.unique().astype(str)))
    conf_matrix = sklearn.metrics.confusion_matrix(target, prediction_labels)
    confusion_by_classes = calculate_confusion_by_classes(conf_matrix, labels)
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[dict] = None

    # calculate rates metrics and plot data
    if class_num == 2 and pos_label is not None:
        conf_by_pos_label = confusion_by_classes[str(pos_label)]
        tpr = conf_by_pos_label["tp"] / (conf_by_pos_label["tp"] + conf_by_pos_label["fn"])
        tnr = conf_by_pos_label["tn"] / (conf_by_pos_label["tn"] + conf_by_pos_label["fp"])
        fpr = conf_by_pos_label["fp"] / (conf_by_pos_label["fp"] + conf_by_pos_label["tn"])
        fnr = conf_by_pos_label["fn"] / (conf_by_pos_label["fn"] + conf_by_pos_label["tp"])

    if class_num == 2 and prediction_probas is not None and roc_curve is not None:
        rate_plots_data = {
            "thrs": roc_curve[pos_label]["thrs"],
            "tpr": roc_curve[pos_label]["tpr"],
            "fpr": roc_curve[pos_label]["fpr"],
        }

        df = pd.DataFrame({"true": binaraized_target[pos_label].values, "preds": prediction_probas[pos_label].values})
        tnrs = []
        fnrs = []
        for tr in rate_plots_data["thrs"]:
            if tr < 1:
                tn = df[(df.true == 0) & (df.preds < tr)].shape[0]
                fn = df[(df.true == 1) & (df.preds < tr)].shape[0]
                tp = df[(df.true == 1) & (df.preds >= tr)].shape[0]
                fp = df[(df.true == 0) & (df.preds >= tr)].shape[0]
                tnrs.append(tn / (tn + fp))
                fnrs.append(fn / (fn + tp))
            else:
                fnrs.append(1)
                tnrs.append(1)
        rate_plots_data["fnr"] = fnrs
        rate_plots_data["tnr"] = tnrs

    return DatasetClassificationPerformanceMetrics(
        accuracy=accuracy_score,
        precision=avg_precision,
        recall=avg_recall,
        f1=avg_f1,
        roc_auc=roc_auc,
        log_loss=log_loss,
        metrics_matrix=metrics_matrix,
        confusion_matrix=ConfusionMatrix(labels=labels, values=conf_matrix.tolist()),
        roc_aucs=roc_aucs,
        roc_curve=roc_curve,
        confusion_by_classes=confusion_by_classes,
        tpr=tpr,
        tnr=tnr,
        fpr=fpr,
        fnr=fnr,
        rate_plots_data=rate_plots_data,
    )


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceResults]):
    def calculate(self, data: InputData) -> ClassificationPerformanceResults:
        if data.reference_data is None:
            columns = process_columns(data.current_data, data.column_mapping)

        else:
            columns = process_columns(data.reference_data, data.column_mapping)

        current_data = _cleanup_data(data.current_data, data.column_mapping)
        target_data = current_data[data.column_mapping.target]
        predictions = get_prediction_data(current_data, columns, pos_label=data.column_mapping.pos_label)
        prediction_data = predictions.predictions
        prediction_probas = predictions.prediction_probas

        current_metrics = classification_performance_metrics(
            target_data, prediction_data, prediction_probas, data.column_mapping.pos_label
        )

        # data for plots
        if prediction_probas is not None:
            current_metrics.plot_data = _collect_plot_data(prediction_probas)
        reference_metrics = None

        if data.reference_data is not None:
            reference_data = _cleanup_data(data.reference_data, data.column_mapping)
            ref_predictions = get_prediction_data(reference_data, columns, pos_label=data.column_mapping.pos_label)
            ref_prediction_data = ref_predictions.predictions
            ref_probas = ref_predictions.prediction_probas
            ref_target = reference_data[data.column_mapping.target]
            reference_metrics = classification_performance_metrics(
                ref_target,
                ref_prediction_data,
                ref_probas,
                data.column_mapping.pos_label,
            )
            if ref_probas is not None:
                reference_metrics.plot_data = _collect_plot_data(ref_probas)

        # dummy
        labels_ratio = target_data.value_counts(normalize=True)
        np.random.seed(0)
        dummy_preds = np.random.choice(labels_ratio.index, len(target_data), p=labels_ratio)
        dummy_metrics = classification_performance_metrics(
            target_data, dummy_preds, None, data.column_mapping.pos_label
        )

        # dummy log_loss
        if prediction_probas is not None:
            binaraized_target = (
                target_data.astype(str).values.reshape(-1, 1) == list(prediction_probas.columns.astype(str))
            ).astype(int)
            dummy_prediction = np.full(prediction_probas.shape, 1 / prediction_probas.shape[1])
            dummy_log_loss = sklearn.metrics.log_loss(binaraized_target, dummy_prediction)
            dummy_metrics.log_loss = dummy_log_loss

        dummy_metrics.roc_auc = 0.5

        return ClassificationPerformanceResults(
            columns=columns,
            current=current_metrics,
            reference=reference_metrics,
            dummy=dummy_metrics,
        )


@default_renderer(wrap_type=ClassificationPerformanceMetrics)
class ClassificationPerformanceMetricsRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationPerformanceMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_metrics_table(dataset_name: str, metrics: DatasetClassificationPerformanceMetrics) -> BaseWidgetInfo:
        counters = [
            CounterData.float("Accuracy", metrics.accuracy, 3),
            CounterData.float("Precision", metrics.precision, 3),
            CounterData.float("Recall", metrics.recall, 3),
            CounterData.float("F1", metrics.f1, 3),
        ]

        if metrics.roc_auc is not None:
            counters.append(CounterData.float(label="ROC AUC", value=metrics.roc_auc, precision=3))

        if metrics.log_loss is not None:
            counters.append(CounterData.float(label="LogLoss", value=metrics.log_loss, precision=3))

        return counter(
            counters=counters,
            title=f"{dataset_name.capitalize()}: Model Quality With Macro-average Metrics",
        )

    def _get_class_representation_graph(
        self,
        dataset_name: str,
        metrics: DatasetClassificationPerformanceMetrics,
        size: WidgetSize,
        columns: DatasetColumns,
    ) -> BaseWidgetInfo:
        metrics_frame = pd.DataFrame(metrics.metrics_matrix)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=columns.target_names if columns.target_names else metrics_frame.columns.tolist()[:-3],
                y=metrics_frame.iloc[-1:, :-3].values[0],
                marker_color=self.color_options.primary_color,
                name="Support",
            )
        )
        fig.update_layout(
            xaxis_title="Class",
            yaxis_title="Number of Objects",
        )
        return plotly_figure(
            title=f"{dataset_name.capitalize()}: Class Representation",
            figure=fig,
            size=size,
        )

    @staticmethod
    def _get_confusion_matrix_graph(
        dataset_name: str,
        metrics: DatasetClassificationPerformanceMetrics,
        size: WidgetSize,
    ) -> BaseWidgetInfo:
        conf_matrix = metrics.confusion_matrix.values
        labels = metrics.confusion_matrix.labels
        z = [[int(y) for y in x] for x in conf_matrix]

        # change each element of z to type string for annotations
        z_text = [[str(y) for y in x] for x in z]

        fig = ff.create_annotated_heatmap(
            z, x=labels, y=labels, annotation_text=z_text, colorscale="bluered", showscale=True
        )

        fig.update_layout(xaxis_title="Predicted value", yaxis_title="Actual value")

        return plotly_figure(title=f"{dataset_name.capitalize()}: Confusion Matrix", figure=fig, size=size)

    @staticmethod
    def _get_metrics_matrix_graph(
        dataset_name: str, metrics: DatasetClassificationPerformanceMetrics, size: WidgetSize, columns: DatasetColumns
    ) -> BaseWidgetInfo:
        # plot support bar
        metrics_matrix = metrics.metrics_matrix
        metrics_frame = pd.DataFrame(metrics_matrix)

        z = metrics_frame.iloc[:-1, :-3].values
        x = columns.target_names if columns.target_names else metrics_frame.columns.tolist()[:-3]
        y = ["precision", "recall", "f1-score"]

        # change each element of z to type string for annotations
        z_text = [[str(round(y, 3)) for y in x] for x in z]

        # set up figure
        fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale="bluered", showscale=True)
        fig.update_layout(xaxis_title="Class", yaxis_title="Metric")

        return plotly_figure(title=f"{dataset_name.capitalize()}: Quality Metrics by Class", figure=fig, size=size)

    def render_html(self, obj: ClassificationPerformanceMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        columns = metric_result.columns
        target_name = columns.utility_columns.target
        result = [
            header_text(label=f"Classification Model Performance. Target: '{target_name}'"),
        ]
        # add tables with perf metrics
        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        result.append(self._get_metrics_table(dataset_name="current", metrics=metric_result.current))

        if metric_result.reference is not None:
            size = WidgetSize.HALF

        else:
            size = WidgetSize.FULL

        # add graphs with class representation
        if metric_result.reference is not None:
            result.append(
                self._get_class_representation_graph(
                    dataset_name="reference",
                    metrics=metric_result.reference,
                    size=WidgetSize.HALF,
                    columns=columns,
                )
            )

        result.append(
            self._get_class_representation_graph(
                dataset_name="current",
                metrics=metric_result.current,
                size=size,
                columns=columns,
            )
        )

        # add confusion matrix graph
        if metric_result.reference is not None:
            result.append(
                self._get_confusion_matrix_graph(
                    dataset_name="reference", metrics=metric_result.reference, size=WidgetSize.HALF
                )
            )

        result.append(
            self._get_confusion_matrix_graph(dataset_name="current", metrics=metric_result.current, size=size)
        )

        # add metrix matrix graph by classes
        # add confusion matrix graph
        if metric_result.reference is not None:
            result.append(
                self._get_metrics_matrix_graph(
                    dataset_name="reference", metrics=metric_result.reference, size=WidgetSize.HALF, columns=columns
                )
            )

        result.append(
            self._get_metrics_matrix_graph(
                dataset_name="current", metrics=metric_result.current, size=size, columns=columns
            )
        )
        return result


def _dummy_threshold_metrics(
    threshold: float, dummy_results: DatasetClassificationPerformanceMetrics
) -> DatasetClassificationPerformanceMetrics:
    if threshold == 1.0:
        mult_precision = 1.0
    else:
        mult_precision = min(1.0, 0.5 / (1 - threshold))
    mult_recall = min(1.0, (1 - threshold) / 0.5)

    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    if (
        dummy_results.tpr is not None
        and dummy_results.tnr is not None
        and dummy_results.fpr is not None
        and dummy_results.fnr is not None
    ):
        tpr = dummy_results.tpr * mult_recall
        tnr = dummy_results.tnr * mult_precision
        fpr = dummy_results.fpr * mult_recall
        fnr = dummy_results.fnr * mult_precision

    return DatasetClassificationPerformanceMetrics(
        accuracy=dummy_results.accuracy,
        precision=dummy_results.precision * mult_precision,
        recall=dummy_results.recall * mult_recall,
        f1=2
        * dummy_results.precision
        * mult_precision
        * dummy_results.recall
        * mult_recall
        / (dummy_results.precision * mult_precision + dummy_results.recall * mult_recall),
        roc_auc=None,
        log_loss=dummy_results.log_loss,
        metrics_matrix=dummy_results.metrics_matrix,
        confusion_matrix=dummy_results.confusion_matrix,
        confusion_by_classes=dummy_results.confusion_by_classes,
        tpr=tpr,
        tnr=tnr,
        fpr=fpr,
        fnr=fnr,
    )


class ClassificationPerformanceMetricsThresholdBase(Metric[ClassificationPerformanceResults]):
    def calculate(self, data: InputData) -> ClassificationPerformanceResults:
        if data.reference_data is None:
            columns = process_columns(data.current_data, data.column_mapping)
        else:
            columns = process_columns(data.reference_data, data.column_mapping)

        current_data = _cleanup_data(data.current_data, data.column_mapping)
        target_data = current_data[data.column_mapping.target]
        threshold = self.get_threshold(current_data, data.column_mapping)
        current_results = self.calculate_metric(data.current_data, data.column_mapping)

        # dummy
        labels_ratio = target_data.value_counts(normalize=True)
        np.random.seed(0)
        dummy_preds = np.random.choice(labels_ratio.index, len(target_data), p=labels_ratio)
        dummy_metrics = classification_performance_metrics(
            target_data, dummy_preds, None, data.column_mapping.pos_label
        )
        dummy_results = _dummy_threshold_metrics(threshold, dummy_metrics)
        reference_results = None
        if data.reference_data is not None:
            reference_results = self.calculate_metric(data.reference_data, data.column_mapping)
        return ClassificationPerformanceResults(
            columns=columns,
            current=current_results,
            dummy=dummy_results,
            reference=reference_results,
        )

    @abc.abstractmethod
    def get_threshold(self, dataset: pd.DataFrame, mapping: ColumnMapping) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_metric(self, dataset: pd.DataFrame, mapping: ColumnMapping):
        raise NotImplementedError()


class ClassificationPerformanceMetricsTopK(ClassificationPerformanceMetricsThresholdBase):
    def __init__(self, k: Union[float, int]):
        self.k = k

    def get_threshold(self, dataset: pd.DataFrame, columns: ColumnMapping) -> float:
        processed_columns = process_columns(dataset, columns)
        predictions = get_prediction_data(dataset, processed_columns, pos_label=columns.pos_label)

        if predictions.prediction_probas is None:
            raise ValueError("Top K parameter can be used only with binary classification with probas")

        return k_probability_threshold(predictions.prediction_probas, self.k)

    def calculate_metric(self, dataset: pd.DataFrame, mapping: ColumnMapping):
        data = _cleanup_data(dataset, mapping)
        target_data = data[mapping.target]
        columns = process_columns(dataset, mapping)
        predictions = get_prediction_data(data, columns, pos_label=mapping.pos_label)
        labels = sorted(set(target_data.unique()))
        prediction_probas = predictions.prediction_probas
        return _calculate_k_variant(target_data, prediction_probas, labels, self.k)

    def get_parameters(self) -> tuple:
        return tuple((self.k,))


@default_renderer(wrap_type=ClassificationPerformanceMetricsTopK)
class ClassificationPerformanceMetricsTopKRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationPerformanceMetricsTopK) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_metrics_table(dataset_name: str, metrics: DatasetClassificationPerformanceMetrics) -> BaseWidgetInfo:
        counters = [
            CounterData.float("Accuracy", metrics.accuracy, 3),
            CounterData.float("Precision", metrics.precision, 3),
            CounterData.float("Recall", metrics.recall, 3),
            CounterData.float("F1", metrics.f1, 3),
        ]

        return counter(
            title=f"{dataset_name.capitalize()}: Model Quality With Macro-average Metrics",
            counters=counters,
        )

    def render_html(self, obj: ClassificationPerformanceMetricsTopK) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label=f"Classification Performance With Top K (k={obj.k})"),
            self._get_metrics_table(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        return result


class ClassificationPerformanceMetricsThreshold(ClassificationPerformanceMetricsThresholdBase):
    def __init__(self, classification_threshold: float):
        self.threshold = classification_threshold

    def get_threshold(self, dataset: pd.DataFrame, mapping: ColumnMapping) -> float:
        return self.threshold

    def calculate_metric(self, dataset: pd.DataFrame, mapping: ColumnMapping):
        data = _cleanup_data(dataset, mapping)
        target_data = data[mapping.target]
        columns = process_columns(dataset, mapping)
        predictions = get_prediction_data(data, columns, pos_label=mapping.pos_label)
        prediction_probas = predictions.prediction_probas
        return _calculate_threshold(target_data, prediction_probas, self.threshold)

    def get_parameters(self) -> tuple:
        return tuple((self.threshold,))


@default_renderer(wrap_type=ClassificationPerformanceMetricsThreshold)
class ClassificationPerformanceMetricsThresholdRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationPerformanceMetricsThreshold) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_metrics_table(
        dataset_name: str,
        metrics: DatasetClassificationPerformanceMetrics,
    ) -> BaseWidgetInfo:
        counters = [
            CounterData.float("Accuracy", metrics.accuracy, 3),
            CounterData.float("Precision", metrics.precision, 3),
            CounterData.float("Recall", metrics.recall, 3),
            CounterData.float("F1", metrics.f1, 3),
        ]

        return counter(
            title=f"{dataset_name.capitalize()}: Model Quality With Macro-average Metrics",
            counters=counters,
        )

    def render_html(self, obj: ClassificationPerformanceMetricsThreshold) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label=f"Classification Performance With Threshold (threshold={obj.threshold})"),
            self._get_metrics_table(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        return result


def _cleanup_data(data: pd.DataFrame, mapping: ColumnMapping) -> pd.DataFrame:
    target = mapping.target
    prediction = mapping.prediction
    subset = []
    if target is not None:
        subset.append(target)
    if prediction is not None and isinstance(prediction, list):
        subset += prediction
    if prediction is not None and isinstance(prediction, str):
        subset.append(prediction)
    if len(subset) > 0:
        return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any", subset=subset)
    return data


def _collect_plot_data(prediction_probas: pd.DataFrame):
    res = {}
    mins = []
    lowers = []
    means = []
    uppers = []
    maxs = []
    for col in prediction_probas.columns:
        mins.append(np.percentile(prediction_probas[col], 0))
        lowers.append(np.percentile(prediction_probas[col], 25))
        means.append(np.percentile(prediction_probas[col], 50))
        uppers.append(np.percentile(prediction_probas[col], 75))
        maxs.append(np.percentile(prediction_probas[col], 100))
    res["mins"] = mins
    res["lowers"] = lowers
    res["means"] = means
    res["uppers"] = uppers
    res["maxs"] = maxs
    return res
