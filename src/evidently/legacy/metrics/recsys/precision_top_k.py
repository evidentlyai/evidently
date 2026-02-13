from typing import ClassVar
from typing import Optional

from evidently.legacy.metrics.recsys.base_top_k import TopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer


class PrecisionTopKMetric(TopKMetric):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric:PrecisionTopKMetric"

    def key(self):
        return "precision"


@default_renderer(wrap_type=PrecisionTopKMetric)
class PrecisionTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "precision@k"
    header = "Precision"
