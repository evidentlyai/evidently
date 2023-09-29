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


class PrecisionTopKMetricResult(MetricResult):
    k: int
    current: pd.Series
    reference: Optional[pd.Series] = None


class PrecisionTopKMetric(Metric[PrecisionTopKMetricResult]):
    """Calculates precision top k for recsys"""

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
        super().__init__(options=options)

    def calculate(self, data: InputData) -> PrecisionTopKMetricResult:
        
        target_column = data.data_definition.get_target_column()
        prediction = data.data_definition.get_prediction_columns()
        if target_column is None or prediction is None:
            raise ValueError("Target and prediction were not found in data.")
        _, target_current, target_reference = data.get_data(target_column.column_name)
        if data.column_mapping.recomendations_type == "rank":
            pred_name = prediction.predicted_values.column_name
        else:
            pred_name = prediction.prediction_probas[0].column_name
        _, prediction_current, prediction_reference = data.get_data(pred_name)
        user_column = data.column_mapping.user_id
        if user_column is None:
            raise ValueError("User_id was not found in data.")
        _, user_current, user_reference = data.get_data(user_column)
        curr = collect_dataset(user_current, target_current, prediction_current, self.min_rel_score, self.judged_only)
        ref: Optional[pd.DataFrame] = None
        if user_reference is not None and target_reference is not None and prediction_reference is not None:
            ref = collect_dataset(
                user_reference, target_reference, prediction_reference, self.min_rel_score, self.judged_only
            )
        reference: Optional[pd.Series] = None
        if ref is not None:
            reference = self.calc_result(ref, data.column_mapping.recomendations_type)
        return PrecisionTopKMetricResult(
            k=self.k,
            reference=reference,
            current=self.calc_result(curr, data.column_mapping.recomendations_type)
        )


    def calc_result(self, df, recomendations_type):
        if recomendations_type == 'score':
            df['preds'] = df.groupby('users')['preds'].transform('rank', ascending=False)
        k_max =  max(self.k, min(10, df.groupby('users').agg('size').min()))
        res = []
        for i in range(k_max):
            res.append(df.groupby('users')[['target', 'preds']].apply(
                lambda x: x[x.preds <= i + 1].target.sum()/min(i + 1, len(x))).mean())
        return pd.Series(data=res, index=[i + 1 for i in range(k_max)])


@default_renderer(wrap_type=PrecisionTopKMetric)
class PrecisionTopKMetricRenderer(MetricRenderer):

    def render_html(self, obj: PrecisionTopKMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        k = metric_result.k
        counters = [CounterData.float(label="current", value=metric_result.current[k], precision=3)]
        if metric_result.reference is not None:
            counters.append(CounterData.float(label="reference", value=metric_result.reference[k], precision=3))
        fig = plot_metric_k(metric_result.current, metric_result.reference, "precision@k")

        return [
            header_text(label=f"Precision@{k}."),
            counter(counters=counters),
            plotly_figure(title="", figure=fig)
        ]
