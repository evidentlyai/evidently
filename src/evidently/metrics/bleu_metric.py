import numpy as np
import pandas as pd
from typing import List, Optional, Tuple
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from evidently.base_metric import InputData, Metric, MetricResult
from evidently.core import IncludeTags
from evidently.metric_results import ColumnMetricResult
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text, table_data


class BLEUMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:BLEUMetricResult"
        field_tags = {
            "bleu_scores": {IncludeTags.Current},
            "average_bleu_score": {IncludeTags.Current},
        }

    bleu_scores: List[float]
    average_bleu_score: float


class BLEUMetric(Metric[BLEUMetricResult]):
    class Config:
        type_alias = "evidently:metric:BLEUMetric"

    def __init__(self, reference_column: str, hypothesis_column: str, options: Optional[dict] = None):
        self.reference_column = reference_column
        self.hypothesis_column = hypothesis_column
        super().__init__(options=options)

    def calculate(self, data: InputData) -> BLEUMetricResult:
        reference_texts = data.current_data[self.reference_column]
        hypothesis_texts = data.current_data[self.hypothesis_column]

        bleu_scores = [
            sentence_bleu([ref.split()], hyp.split(), smoothing_function=SmoothingFunction().method1)
            for ref, hyp in zip(reference_texts, hypothesis_texts)
        ]
        average_bleu_score = np.mean(bleu_scores)

        return BLEUMetricResult(bleu_scores=bleu_scores, average_bleu_score=average_bleu_score)


@default_renderer(wrap_type=BLEUMetric)
class BLEUMetricRenderer(MetricRenderer):
    def render_html(self, obj: BLEUMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        headers = ["Row", "BLEU Score"]
        data = [[i, score] for i, score in enumerate(result.bleu_scores)]
        data.append(["Average", result.average_bleu_score])

        return [
            header_text(label="BLEU Scores"),
            table_data(column_names=headers, data=data, title="BLEU Scores per Row"),
        ]
