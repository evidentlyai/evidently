from typing import List
from typing import Union

import evaluate
import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeTags
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


class ROUGESummaryMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ROUGESummaryMetricResult"
        field_tags = {
            "rouge_type": {IncludeTags.Parameter},
            "value": {IncludeTags.Parameter},
        }

    rouge_type: str
    score: dict


class ROUGESummaryMetric(Metric[ROUGESummaryMetricResult]):
    class Config:
        type_alias = "evidently:metric:ROUGESummaryMetric"
        arbitrary_types_allowed = True

    column_name: str
    rouge_n: int

    def __init__(self, column_name: Union[str, ColumnName], rouge_n: int):
        self.column_name = column_name
        self.rouge_n = rouge_n
        super().__init__()

    def _calculate_summary_rouge(self, current_data: pd.Series, reference_data: pd.Series):
        rouge_evaluator = evaluate.load("rouge")

        predictions = current_data.astype(str).tolist()
        references = reference_data.astype(str).tolist()

        rouge_scores = rouge_evaluator.compute(
            rouge_types=[f"rouge{self.rouge_n}"], predictions=predictions, references=references, use_aggregator=False
        )

        per_row_rouge_scores = rouge_scores[f"rouge{self.rouge_n}"]

        summary_rouge_score = sum(per_row_rouge_scores) / len(per_row_rouge_scores)

        return per_row_rouge_scores, summary_rouge_score

    def calculate(self, data: InputData) -> MetricResult:
        if len(data.current_data[self.column_name]) == 0 or len(data.reference_data[self.column_name]) == 0:
            raise ValueError("The current data or the reference data is empty.")

        per_row_rouge_scores, summary_rouge_score = self._calculate_summary_rouge(
            data.current_data[self.column_name], data.reference_data[self.column_name]
        )

        result = ROUGESummaryMetricResult(
            rouge_type=f"ROUGE-{self.rouge_n}",
            score={"per_row_scores": per_row_rouge_scores, "summary_score": summary_rouge_score},
        )
        return result


@default_renderer(wrap_type=ROUGESummaryMetric)
class ROUGESummaryMetricRenderer(MetricRenderer):
    @staticmethod
    def _get_table(metric, n: int = 2) -> BaseWidgetInfo:
        column_names = ["Metric", "Value"]
        rows = ([metric.rouge_type, metric.score],)
        return table_data(title="", column_names=column_names, data=rows)

    def render_html(self, obj: ROUGESummaryMetricResult) -> List[BaseWidgetInfo]:
        metric = obj.get_result()
        return [header_text(label="ROUGE Metric"), self._get_table(metric)]
