from typing import List
from typing import Optional
from typing import Union

import pandas as pd
import pytest
from evidently.calculations import define_predictions_type


@pytest.mark.parametrize(
    "prediction_column, current_data, reference_data, threshold, expected_prediction_column",
    (
        (None, pd.DataFrame({}), pd.DataFrame({}), 0.0, None),
        ("preds", pd.DataFrame({"preds": [1, 2, 3]}), pd.DataFrame({"preds": [1, 2, 3]}), 0.0, "preds"),
        (
            ["pred_a", "pred_b"],
            pd.DataFrame({"pred_a": [1, 0, 1], "pred_b": [1, 0, 1]}),
            pd.DataFrame({"pred_a": [1, 0, 1], "pred_b": [1, 0, 1]}),
            0.0,
            "predicted_labels",
        ),
        (
            ["pred_a", "pred_b", "pred_c", "pred_d"],
            pd.DataFrame(
                {
                    "pred_a": [0.5, 0, 0.8],
                    "pred_b": [0, 0.2, 0.5],
                    "pred_c": [0.3, 0.2, 0.5],
                    "pred_d": [0.1, 0.1, 0.9],
                }
            ),
            pd.DataFrame(
                {
                    "pred_a": [1, 0, 0, 0],
                    "pred_b": [0, 1, 0, 0],
                    "pred_c": [0, 0, 1, 0],
                    "pred_d": [0, 0, 0, 1],
                }
            ),
            0.3,
            "predicted_labels",
        ),
    ),
)
def test_define_predictions_type(
    prediction_column: Optional[Union[str, List]],
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    threshold: float,
    expected_prediction_column: Optional[str],
):
    result = define_predictions_type(
        prediction_column=prediction_column,
        current_data=current_data,
        reference_data=reference_data,
        threshold=threshold,
    )
    assert result == expected_prediction_column

    # check that string prediction column or a new predicted_labels is in datasets
    if prediction_column is not None:
        assert result in current_data
        assert result in reference_data
