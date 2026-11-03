from typing import List
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.calculations.recommender_systems import get_curr_and_ref_df
from evidently.legacy.core import IncludeTags
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.renderers.html_widgets import plotly_figure
from evidently.legacy.utils.visualizations import plot_metric_k


class HitRateKMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:HitRateKMetricResult"
        field_tags = {
            "current": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "k": {IncludeTags.Parameter},
        }

    k: int
    current: pd.Series
    reference: Optional[pd.Series] = None

    @property
    def current_value(self) -> float:
        # JSON snapshot restoration may turn pandas index labels into strings.
        return float(self.current.iloc[self.k - 1])

    @property
    def reference_value(self) -> Optional[float]:
        if self.reference is None:
            return None
        return float(self.reference.iloc[self.k - 1])


class HitRateKMetric(Metric[HitRateKMetricResult]):
    class Config:
        type_alias = "evidently:metric:HitRateKMetric"

    k: int
    min_rel_score: Optional[int]
    no_feedback_users: bool

    def __init__(
        self, k: int, min_rel_score: Optional[int] = None, no_feedback_users: bool = False, options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        super().__init__(options=options)

    def get_values(self, df, max_k):
        user_num = df.users.nunique()
        res = []
        for k in range(1, max_k + 1):
            df_k = df[(df.target == 1) & (df.preds <= k)]
            res.append(df_k.users.nunique() / user_num)
        return pd.Series(data=res)

    def calculate(self, data: InputData) -> HitRateKMetricResult:
        curr, ref = get_curr_and_ref_df(data, self.min_rel_score, self.no_feedback_users, True)
        max_k = min(curr["preds"].max(), max(10, self.k))
        current = self.get_values(curr, max_k)
        reference: Optional[pd.Series] = None
        if ref is not None:
            reference = self.get_values(ref, max_k)
        return HitRateKMetricResult(k=self.k, reference=reference, current=current)


@default_renderer(wrap_type=HitRateKMetric)
class HitRateKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "HitRate@k"
    header = "Hit Rate"

    def render_html(self, obj: HitRateKMetric) -> List[BaseWidgetInfo]:
        # Use positional indexing for results loaded from JSON snapshots.
        result = obj.get_result()
        counters = [CounterData.float(label="current", value=result.current_value, precision=3)]
        if result.reference_value is not None:
            counters.append(CounterData.float(label="reference", value=result.reference_value, precision=3))

        feedback = " No feedback users included." if obj.no_feedback_users else " No feedback users excluded."
        return [
            header_text(label=self.header + f" (top-{result.k})." + feedback),
            counter(counters=counters),
            plotly_figure(
                title="",
                figure=plot_metric_k(result.current, result.reference, self.yaxis_name),
            ),
        ]
