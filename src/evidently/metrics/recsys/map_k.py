from typing import List
from typing import Optional

import pandas as pd

from evidently.base_metric import InputData
from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.metrics.recsys.base_top_k import TopKMetricResult


class MAPKMetric(TopKMetric):
    def calculate(self, data: InputData) -> TopKMetricResult:
        result = self._precision_recall_calculation.get_result()
        key = 'map'
        if self.judged_only:
            key = 'map_judged_only'
        current = pd.Series(
            index = result.current['k'],
            data = result.current[key]
        )
        ref_data = result.reference
        reference: Optional[pd.Series] = None
        if ref_data is not None:
            reference = pd.Series(
            index = ref_data['k'],
            data = ref_data[key]
        )
        return TopKMetricResult(
            k=self.k,
            reference=reference,
            current=current
        )


@default_renderer(wrap_type=MAPKMetric)
class PrecisionTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "map@k"
    header = "MAP@"
