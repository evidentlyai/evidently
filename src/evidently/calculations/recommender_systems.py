from typing import Optional
import pandas as pd
from sklearn import metrics

def collect_dataset(
    users: pd.Series, target: pd.Series, preds: pd.Series, min_rel_score: Optional[int] = None, judged_only: bool = True
):
    df = pd.concat([users, target, preds], axis=1)
    df.columns = ['users', 'target', 'preds']
    if min_rel_score:
        df['target'] = (df['target'] >= min_rel_score).astype(int)
    if judged_only:
        is_judged = df.groupby('users').target.apply(lambda x: x.sum())
        non_judged = is_judged[is_judged==0].index
        df = df[~df.users.isin(non_judged)]
    return df

def precision_top_k(true: pd.Series, preds: pd.Series, k):
    preds_new = (true <= k).astype(int)
    return metrics.precision_score(true, preds_new)