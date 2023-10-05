from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
import numpy as np

from evidently.base_metric import Metric
from evidently.base_metric import InputData
from evidently.base_metric import MetricResult
from evidently.options.base import AnyOptions
from evidently.calculations.recommender_systems import collect_dataset


class PrecisionRecallCalculationResult(MetricResult):
    current: Dict[str, list]
    reference: Optional[Dict[str, list]] = None


class PrecisionRecallCalculation(Metric[PrecisionRecallCalculationResult]):
    max_k: int
    min_rel_score: Optional[int]

    def __init__(
        self, 
        max_k: int,
        min_rel_score: Optional[int] = None,
        options: AnyOptions = None
    ) -> None:
        self.max_k = max_k
        self.min_rel_score=min_rel_score
        super().__init__(options=options)

    def get_precision_and_recall_dict(self, df, max_k):
        user_df = df.groupby('users').target.agg(['size', 'sum'])
        user_df.columns = ['size', 'all']
        max_k = min(user_df['size'].max(), max_k)
        res = {}
        for k in range(1, max_k + 1):
            tp = df[df.preds <= k].groupby('users').target.sum().rename(f'tp_{k}')
            user_df = pd.concat([user_df, tp], axis=1).fillna(0)
            user_df[f'precision_{k}'] = user_df[f'tp_{k}'] / np.minimum(user_df['size'], k)
            user_df[f'recall_{k}'] = user_df[f'tp_{k}'] / user_df['all']
        res['k'] = [k for k in range(1, max_k + 1)]
        res['precision'] = list(user_df[[f'precision_{k}' for k in range(1, k + 1)]].mean())
        res['precision_judged_only'] = list(
            user_df.loc[user_df['all'] != 0, [f'precision_{k}' for k in range(1, k + 1)]].mean()
        )
        res['map'] = list(
            user_df[[f'precision_{k}' for k in range(1, k + 1)]].expanding(axis=1).mean().mean()
        )
        res['map_judged_only'] = list(
            user_df.loc[user_df['all'] != 0, [f'precision_{k}' for k in range(1, k + 1)]].expanding(axis=1).mean().mean()
        )
        res['recall'] = list(
            user_df.loc[user_df['all'] != 0, [f'recall_{k}' for k in range(1, k + 1)]].mean()
        )
        res['mar'] = list(
            user_df.loc[user_df['all'] != 0, [f'recall_{k}' for k in range(1, k + 1)]].expanding(axis=1).mean().mean()
        )
        return res

    def calculate(self, data: InputData) -> PrecisionRecallCalculationResult:
        curr, ref = self.get_curr_and_ref_df(data)
        current = self.get_precision_and_recall_dict(curr, self.max_k)
        reference: Optional[dict] = None
        if ref is not None:
            reference = self.get_precision_and_recall_dict(ref, self.max_k)

        return PrecisionRecallCalculationResult(
            current=current,
            reference=reference,
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
