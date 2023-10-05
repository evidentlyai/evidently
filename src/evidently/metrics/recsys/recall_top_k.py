from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer


class RecallTopKMetric(TopKMetric):
    key = 'recall'


@default_renderer(wrap_type=RecallTopKMetric)
class RecallTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "recall@k"
    header = "Recall@"
