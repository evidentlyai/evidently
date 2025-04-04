from typing import Optional

import numpy as np
import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.calculations.recommender_systems import get_curr_and_ref_df
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.legacy.metrics.recsys.base_top_k import TopKMetricResult
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.renderers.base_renderer import default_renderer


class NDCGKMetric(Metric[TopKMetricResult]):
    class Config:
        type_alias = "evidently:metric:NDCGKMetric"

    k: int
    min_rel_score: Optional[int]
    no_feedback_users: bool

    def __init__(
        self, k: int, min_rel_score: Optional[int] = None, no_feedback_users: bool = False, options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        super().__init__(options=options)

    def calculate(self, data: InputData) -> TopKMetricResult:
        curr, ref = get_curr_and_ref_df(data, self.min_rel_score, self.no_feedback_users, False)
        current = self.calculate_ndcg(curr, self.k)
        reference: Optional[pd.Series] = None
        if ref is not None:
            reference = self.calculate_ndcg(ref, self.k)

        return TopKMetricResult(
            k=self.k,
            current=current,
            reference=reference,
        )

    def calculate_ndcg(self, df, k):
        df = df.copy()
        # users_with_int = df[df.target > 0].users.unique()
        # df = df[df.users.isin(users_with_int)]
        df["dcg"] = df["target"] / np.log2(df["preds"] + 1)
        max_k = int(min(df["preds"].max(), max(k, 10)))
        df = df.sort_values(["users", "target"], ascending=False)
        ndcg_k = []
        for i in range(1, max_k + 1):
            discount = 1 / np.log2(np.arange(i) + 2)
            dcg = df[df.preds <= i].groupby("users").dcg.sum()
            idcg = df.groupby("users").target.apply(lambda x: x[:i].dot(discount[: len(x)])).rename("idcg")
            user_df = pd.concat([dcg, idcg], axis=1).fillna(0)
            ndcg_k.append((user_df["dcg"] / user_df["idcg"]).replace([np.inf, -np.inf], np.nan).fillna(0).mean())

        return pd.Series(index=[k for k in range(1, max_k + 1)], data=ndcg_k)


@default_renderer(wrap_type=NDCGKMetric)
class NDCGKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "ndcg@k"
    header = "NDCG"
