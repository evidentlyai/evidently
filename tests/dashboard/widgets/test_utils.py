import pandas as pd
import pytest

from evidently.dashboard.widgets.utils import CutQuantileTransformer


@pytest.mark.parametrize(
    "side, quantile, test_data",
    (
        (
            "right",
            0.50,
            pd.DataFrame({"data": [1, 2, 3, 4]}),
        ),
        ("left", 0.50, pd.DataFrame({"data": [1, 2, 3, 4]})),
        ("right", 1, pd.DataFrame({"data": [1, 2, 3, 4]})),
        ("left", 1, pd.DataFrame({"data": [1, 2, 3, 4]})),
        ("between", 1, pd.DataFrame({"data": [1, 2, 3, 4]})),
        ("between", 1, pd.DataFrame({"data": [1, 2, 3, 4]})),
    ),
)
def test_cut_quantile_transformer(
    side: str,
    quantile: float,
    test_data: pd.DataFrame,
):
    transformer = CutQuantileTransformer(side=side, q=quantile)
    transformer.fit(test_data["data"])
    transformer.transform(test_data["data"])
    transformer.transform_df(test_data, "data")
