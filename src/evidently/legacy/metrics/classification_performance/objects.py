from typing import ClassVar
from typing import Dict
from typing import Optional

from pydantic import Field
from pydantic import TypeAdapter
from sklearn.metrics import classification_report

from evidently.legacy.base_metric import MetricResult
from evidently.legacy.metric_results import Label


class ClassMetric(MetricResult):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ClassMetric"

    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    support: Optional[float] = None


ClassesMetrics = Dict[Label, ClassMetric]


class ClassificationReport(MetricResult):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ClassificationReport"

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
        classes = set(c for c in y_true.unique())
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
        for v in report.values():
            if not isinstance(v, dict):
                continue
            v["f1"] = v.pop("f1-score")
        class_metrics = {str(k): TypeAdapter(ClassMetric).validate_python(report[str(k)]) for k in classes}
        other = {str(k): v for k, v in report.items() if k not in [str(cl) for cl in classes]}
        return TypeAdapter(cls).validate_python({"classes": class_metrics, **other})
