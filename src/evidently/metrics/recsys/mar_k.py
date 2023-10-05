from typing import List
from typing import Optional

import pandas as pd

from evidently.base_metric import InputData
from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.metrics.recsys.base_top_k import TopKMetricResult
from evidently.options.base import AnyOptions
from evidently.metrics.recsys.precision_recall_k import PrecisionRecallCalculation


class MARKMetric(TopKMetric):
    k: int
    min_rel_score: Optional[int]
    _precision_recall_calculation: PrecisionRecallCalculation

    def __init__(
        self,
        k: int,
        min_rel_score: Optional[int] = None,
        options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score=min_rel_score
        self._precision_recall_calculation = PrecisionRecallCalculation(max(k, 10), min_rel_score)
        super().__init__(
            options=options,
            k=k,
            min_rel_score=min_rel_score,
            judged_only=True,
        )

    def calculate(self, data: InputData) -> TopKMetricResult:
        result = self._precision_recall_calculation.get_result()
        current = pd.Series(
            index = result.current['k'],
            data = result.current['mar']
        )
        ref_data = result.reference
        reference: Optional[pd.Series] = None
        if ref_data is not None:
            reference = pd.Series(
            index = ref_data['k'],
            data = ref_data['mar']
        )
        return TopKMetricResult(
            k=self.k,
            reference=reference,
            current=current
        )


@default_renderer(wrap_type=MARKMetric)
class MARKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "mar@k"
    header = "MAR@"
