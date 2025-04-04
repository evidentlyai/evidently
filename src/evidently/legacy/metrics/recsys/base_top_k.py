import abc
from typing import List
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import IncludeTags
from evidently.legacy.metrics.recsys.precision_recall_k import PrecisionRecallCalculation
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.renderers.html_widgets import plotly_figure
from evidently.legacy.utils.visualizations import plot_metric_k


class TopKMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:TopKMetricResult"
        field_tags = {
            "current": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "k": {IncludeTags.Parameter},
        }

    k: int
    current: pd.Series
    current_value: float
    reference: Optional[pd.Series] = None
    reference_value: Optional[float] = None

    def __init__(
        self,
        k: int,
        current: pd.Series,
        current_value: Optional[float] = None,
        reference: Optional[pd.Series] = None,
        reference_value: Optional[float] = None,
    ):
        super().__init__(
            k=k,
            current=current,
            current_value=current_value if current_value is not None else current[k - 1],
            reference=reference,
            reference_value=reference_value if reference_value is not None or reference is None else reference[k - 1],
        )


class TopKMetric(Metric[TopKMetricResult], abc.ABC):
    _precision_recall_calculation: PrecisionRecallCalculation
    k: int
    min_rel_score: Optional[int]
    no_feedback_users: bool

    def __init__(
        self, k: int, min_rel_score: Optional[int] = None, no_feedback_users: bool = False, options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        self._precision_recall_calculation = PrecisionRecallCalculation(max(k, 10), min_rel_score)
        super().__init__(options=options)

    def calculate(self, data: InputData) -> TopKMetricResult:
        result = self._precision_recall_calculation.get_result()
        key = self.key()
        if key is None:
            raise ValueError("Key should be specified")
        if self.no_feedback_users:
            key = f"{self.key()}_include_no_feedback"

        current = pd.Series(data=result.current[key])
        ref_data = result.reference
        reference: Optional[pd.Series] = None
        if ref_data is not None:
            reference = pd.Series(data=ref_data[key])
        return TopKMetricResult(k=self.k, reference=reference, current=current)

    @abc.abstractmethod
    def key(self) -> str:
        raise NotImplementedError()


@default_renderer(wrap_type=TopKMetric)
class TopKMetricRenderer(MetricRenderer):
    yaxis_name: str
    header: str

    def render_html(self, obj: TopKMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        k = metric_result.k
        counters = [CounterData.float(label="current", value=metric_result.current[k - 1], precision=3)]
        if metric_result.reference is not None:
            counters.append(CounterData.float(label="reference", value=metric_result.reference[k - 1], precision=3))
        fig = plot_metric_k(metric_result.current, metric_result.reference, self.yaxis_name)
        header_part = " No feedback users included."
        if not obj.no_feedback_users:
            header_part = " No feedback users excluded."

        return [
            header_text(label=self.header + f" (top-{k})." + header_part),
            counter(counters=counters),
            plotly_figure(title="", figure=fig),
        ]
