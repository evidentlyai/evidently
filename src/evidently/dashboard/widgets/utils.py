import pandas as pd
from plotly.graph_objs import Figure


def fig_to_json(figure: Figure) -> dict:
    result = figure.to_plotly_json()
    result["layout"].pop("template", None)
    return result


class CutQuantileTransformer:
    def __init__(self, side: str, q: float):
        self.side = side
        self.q = q
        self.q_val_left = None
        self.q_val_right = None

    def fit(self, s: pd.Series):
        if self.side == "left":
            self.q_val_left = s.quantile(self.q)
        elif self.side == "right":
            self.q_val_right = s.quantile(self.q)
        else:
            self.q_val_left = s.quantile(self.q)
            self.q_val_right = s.quantile(1 - self.q)

    def transform(self, s: pd.Series):
        if self.side == "left":
            return s[s >= self.q_val_left]
        elif self.side == "right":
            return s[s <= self.q_val_right]
        else:
            return s[s.between(self.q_val_left, self.q_val_right)]

    def transform_df(self, df: pd.DataFrame, feature: str):
        if self.side == "left":
            return df[df[feature] >= self.q_val_left]
        elif self.side == "right":
            return df[df[feature] <= self.q_val_right]
        else:
            return df[df[feature].between(self.q_val_left, self.q_val_right)]
