from typing import Optional
import pandas as pd

def collect_dataset(users: pd.Series, target: pd.Series, preds: pd.Series, min_rel_score: Optional[int] = None):
    df = pd.concat([users, target, preds], axis=1)
    df.columns = ['users', 'target', 'preds']
    if min_rel_score:
        df['target'] = (df['target'] >= min_rel_score).astype(int)
    return df
