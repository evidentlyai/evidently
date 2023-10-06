from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer


class MARKMetric(TopKMetric):
    key = 'mar'


@default_renderer(wrap_type=MARKMetric)
class MARKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "mar@k"
    header = "MAR@"
