from typing import List
from typing import Optional

import pandas as pd

from evidently.base_metric import MetricResult
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.calculations.recommender_systems import collect_dataset
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.visualizations import plot_metric_k
from evidently.metrics.recsys.precision_recall_k import PrecisionRecallCalculation


class TopKMetricResult(MetricResult):
    k: int
    current: pd.Series
    reference: Optional[pd.Series] = None


class TopKMetric(Metric[TopKMetricResult]):
    _precision_recall_calculation: PrecisionRecallCalculation
    k: int
    min_rel_score: Optional[int]
    judged_only: bool

    def __init__(
        self, k: int,
        min_rel_score: Optional[int] = None,
        judged_only: bool = True,
        options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score=min_rel_score
        self.judged_only=judged_only
        self._precision_recall_calculation = PrecisionRecallCalculation(max(k, 10), min_rel_score)
        super().__init__(options=options)


@default_renderer(wrap_type=TopKMetric)
class TopKMetricRenderer(MetricRenderer):
    yaxis_name: str
    header: str
    def render_html(self, obj: TopKMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        k = metric_result.k
        counters = [CounterData.float(label="current", value=metric_result.current[k], precision=3)]
        if metric_result.reference is not None:
            counters.append(CounterData.float(label="reference", value=metric_result.reference[k], precision=3))
        fig = plot_metric_k(metric_result.current, metric_result.reference, self.yaxis_name)

        return [
            header_text(label=self.header + str(k)),
            counter(counters=counters),
            plotly_figure(title="", figure=fig)
        ]
