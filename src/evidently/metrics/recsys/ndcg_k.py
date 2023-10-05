from typing import List
from typing import Optional

import pandas as pd
import numpy as np

from evidently.base_metric import InputData
from evidently.renderers.base_renderer import default_renderer
from evidently.metrics.recsys.base_top_k import TopKMetricRenderer
from evidently.metrics.recsys.base_top_k import TopKMetricResult
from evidently.base_metric import Metric
from evidently.options.base import AnyOptions
from evidently.calculations.recommender_systems import collect_dataset


class NDCGKMetric(Metric[TopKMetricResult]):
    k: int
    min_rel_score: Optional[int]

    def __init__(
        self, k: int,
        min_rel_score: Optional[int] = None,
        options: AnyOptions = None
    ) -> None:
        self.k = k
        self.min_rel_score=min_rel_score
        super().__init__(options=options)
    
    def calculate(self, data: InputData) -> TopKMetricResult:
        curr, ref = self.get_curr_and_ref_df(data)
        current = self.calculate_ndcg(curr, self.k)
        reference: Optional[dict] = None
        if ref is not None:
            reference = self.calculate_ndcg(ref, self.k)

        return TopKMetricResult(
            k=self.k,
            current=current,
            reference=reference,
        )
    
    def calculate_ndcg(self, df, k):
        df = df.copy()
        users_with_int = df[df.target > 0].users.unique()
        df = df[df.users.isin(users_with_int)]
        df['dcg'] = df['target'] / np.log2(df['preds'] + 1)
        max_k = int(min(df['preds'].max(), max(k, 10)))
        df = df.sort_values(['users','target'], ascending=False)
        ndcg_k = []
        for i in range(1, max_k + 1):
            discount = 1 / np.log2(np.arange(i) + 2)
            dcg = df[df.preds <= i].groupby('users').dcg.sum()
            idcg = df[df.preds <= i].groupby('users').target.apply(lambda x: x.dot(discount)).rename('idcg')
            user_df = pd.concat([dcg, idcg], axis=1).fillna(0)
            ndcg_k.append((user_df['dcg'] / user_df['idcg']).fillna(0).mean())

        return pd.Series(
            index=[k for k in range(1, max_k + 1)],
            data=ndcg_k
        )
        
    
    def get_curr_and_ref_df(self, data: InputData):
        target_column = data.data_definition.get_target_column()
        prediction = data.data_definition.get_prediction_columns()
        if target_column is None or prediction is None:
            raise ValueError("Target and prediction were not found in data.")
        _, target_current, target_reference = data.get_data(target_column.column_name)
        recomendations_type = data.column_mapping.recomendations_type
        if recomendations_type == "rank":
            pred_name = prediction.predicted_values.column_name
        else:
            pred_name = prediction.prediction_probas[0].column_name
        _, prediction_current, prediction_reference = data.get_data(pred_name)
        user_column = data.column_mapping.user_id
        if user_column is None:
            raise ValueError("User_id was not found in data.")
        _, user_current, user_reference = data.get_data(user_column)
        curr = collect_dataset(user_current, target_current, prediction_current, self.min_rel_score)
        if recomendations_type == 'score':
            curr['preds'] = curr.groupby('users')['preds'].transform('rank', ascending=False)
        ref: Optional[pd.DataFrame] = None
        if user_reference is not None and target_reference is not None and prediction_reference is not None:
            ref = collect_dataset(user_reference, target_reference, prediction_reference, self.min_rel_score)
            if recomendations_type == 'score':
                ref['preds'] = ref.groupby('users')['preds'].transform('rank', ascending=False)
        return curr, ref


@default_renderer(wrap_type=NDCGKMetric)
class NDCGKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "ndcg@k"
    header = "NDCG@"