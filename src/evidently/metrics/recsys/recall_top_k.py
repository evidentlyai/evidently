from typing import ClassVar

from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.renderers.base_renderer import default_renderer


class RecallTopKMetric(TopKMetric):
    __type_alias__: ClassVar = "evidently:metric:RecallTopKMetric"

    def key(self):
        return "recall"


@default_renderer(wrap_type=RecallTopKMetric)
class RecallTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "recall@k"
    header = "Recall"
