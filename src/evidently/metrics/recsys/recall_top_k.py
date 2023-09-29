from typing import List
from typing import Optional

import pandas as pd

from evidently.base_metric import InputData
from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetric
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.metrics.recsys.base_top_k import TopKMetricResult
from evidently.options.base import AnyOptions

     
class RecallTopKMetric(TopKMetric):
    k: int
    min_rel_score: Optional[int]
    # judged_only: bool

    def __init__(
        self,
        k: int,
        min_rel_score: Optional[int] = None,
        options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score=min_rel_score
        self.judged_only=True
        super().__init__(options=options, k=k, min_rel_score=min_rel_score, judged_only=True)


    def calculate(self, data: InputData) -> TopKMetricResult:
        curr, ref = self.get_curr_and_ref_df(data)
        reference: Optional[pd.Series] = None
        if ref is not None:
            reference = self.calc_result(ref, data.column_mapping.recomendations_type)
        return TopKMetricResult(
            k=self.k,
            reference=reference,
            current=self.calc_result(curr, data.column_mapping.recomendations_type)
        )


    def calc_result(self, df, recomendations_type):
        if recomendations_type == 'score':
            df['preds'] = df.groupby('users')['preds'].transform('rank', ascending=False)
        k_max =  max(self.k, min(10, df.groupby('users').agg('size').min()))
        res = []
        for i in range(k_max):
            res.append(df.groupby('users')[['target', 'preds']].apply(
                lambda x: x[x.preds <= i + 1].target.sum() / x.target.sum()).mean())
        return pd.Series(data=res, index=[i + 1 for i in range(k_max)])


@default_renderer(wrap_type=RecallTopKMetric)
class RecallTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "recall@k"
    header = "Recall@"

