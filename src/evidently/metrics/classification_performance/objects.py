from typing import Dict
from typing import Optional

from pydantic import Field
from pydantic import parse_obj_as
from sklearn.metrics import classification_report

from evidently.base_metric import MetricResultField
from evidently.metric_results import Boxes
from evidently.metric_results import RatesPlotData


class ClassMetric(MetricResultField):
    precision: float
    recall: float
    f1: float = Field(alias="f1-score")
    support: Optional[float] = None


ClassesMetrics = Dict[str, ClassMetric]


class ClassificationReport(MetricResultField):
    classes: ClassesMetrics
    accuracy: float
    macro_avg: ClassMetric = Field(alias="macro avg")
    weighted_avg: ClassMetric = Field(alias="weighted avg")

    @classmethod
    def create(
        cls,
        y_true,
        y_pred,
        *,
        class_metrics=None,
        target_names=None,
        sample_weight=None,
        digits=2,
        zero_division="warn",
    ) -> "ClassificationReport":
        classes = set(str(c) for c in y_true.unique())
        report = classification_report(
            y_true,
            y_pred,
            labels=class_metrics,
            target_names=target_names,
            sample_weight=sample_weight,
            digits=digits,
            output_dict=True,
            zero_division=zero_division,
        )
        class_metrics = {k: parse_obj_as(ClassMetric, report[k]) for k in classes}
        other = {k: v for k, v in report.items() if k not in classes}
        return parse_obj_as(cls, {"classes": class_metrics, **other})


class DatasetClassificationQuality(MetricResultField):
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
    rate_plots_data: Optional[RatesPlotData] = None
    plot_data: Optional[Boxes] = None
