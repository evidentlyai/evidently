from typing import ClassVar
from typing import Optional

from evidently.legacy.metrics.recsys.base_top_k import TopKMetric
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer


class MARKMetric(TopKMetric):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric:MARKMetric"

    def key(self):
        return "mar"


@default_renderer(wrap_type=MARKMetric)
class MARKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "mar@k"
    header = "MAR"
