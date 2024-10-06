from typing import List

import evaluate
import pandas as pd

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeTags
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import text_widget


class ROUGESummaryMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ROUGESummaryMetricResult"
        field_tags = {
            "current": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "rouge_type": {IncludeTags.Parameter},
            "per_row_scores": {IncludeTags.Parameter},
            "summary_score": {IncludeTags.Parameter},
        }

    current: list
    reference: list
    rouge_type: str
    per_row_scores: list
    summary_score: float


class ROUGESummaryMetric(Metric[ROUGESummaryMetricResult]):
    class Config:
        type_alias = "evidently:metric:ROUGESummaryMetric"
        arbitrary_types_allowed = True

    column_name: str
    rouge_n: int

    def __init__(self, column_name: str, rouge_n: int, options: AnyOptions = None):
        self.column_name = column_name
        self.rouge_n = rouge_n
        super().__init__(options=options)

    def _calculate_summary_rouge(self, current: pd.Series, reference: pd.Series):
        rouge_evaluator = evaluate.load("rouge")

        current = current.astype(str).tolist()
        reference = reference.astype(str).tolist()

        rouge_scores = rouge_evaluator.compute(
            rouge_types=[f"rouge{self.rouge_n}"], predictions=current, references=reference, use_aggregator=False
        )

        per_row_rouge_scores = rouge_scores[f"rouge{self.rouge_n}"]

        summary_rouge_score = sum(per_row_rouge_scores) / len(per_row_rouge_scores)

        return per_row_rouge_scores, summary_rouge_score, current, reference

    def calculate(self, data: InputData) -> ROUGESummaryMetricResult:
        if data.current_data is None or data.reference_data is None:
            raise ValueError("The current data or the reference data is None.")
        if len(data.current_data[self.column_name]) == 0 or len(data.reference_data[self.column_name]) == 0:
            raise ValueError("The current data or the reference data is empty.")

        per_row_rouge_scores, summary_rouge_score, current, reference = self._calculate_summary_rouge(
            data.current_data[self.column_name], data.reference_data[self.column_name]
        )

        result = ROUGESummaryMetricResult(
            rouge_type=f"ROUGE-{self.rouge_n}",
            per_row_scores=per_row_rouge_scores,
            summary_score=summary_rouge_score,
            current=current,
            reference=reference,
        )
        return result


@default_renderer(wrap_type=ROUGESummaryMetric)
class ROUGESummaryMetricRenderer(MetricRenderer):
    @staticmethod
    def _get_table(metric) -> BaseWidgetInfo:
        column_names = ["Metric", "current", "reference", "score"]
        rows = []
        for i in range(len(metric.current)):
            rows.append([metric.rouge_type, metric.current[i], metric.reference[i], metric.per_row_scores[i]])
        # rows.append(["metric.rouge_type", 1, "metric.current[i]", "metric.reference[i]", 2.4])
        return table_data(title="", column_names=column_names, data=rows)

    def render_html(self, obj: ROUGESummaryMetric) -> List[BaseWidgetInfo]:
        metric = obj.get_result()
        return [
            header_text(label="ROUGE Metric"),
            self._get_table(metric),
            text_widget(text=f"{metric.summary_score}", title="Overall ROUGE score"),
        ]
