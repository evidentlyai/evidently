from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.data_drift import ensure_prediction_column_is_string
from evidently.legacy.calculations.data_drift import get_drift_for_columns
from evidently.legacy.calculations.data_drift import get_one_column_drift
from evidently.legacy.core import ColumnType
from evidently.legacy.options.data_drift import DataDriftOptions
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_operations import process_columns


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
def test_ensure_prediction_column_is_string(
    prediction_column: Optional[Union[str, List]],
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    threshold: float,
    expected_prediction_column: Optional[str],
):
    result = ensure_prediction_column_is_string(
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


@pytest.mark.parametrize(
    "current_data, reference_data, column_name, options, column_type, expected_drift_detected",
    (
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            False,
        ),
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            False,
        ),
        (
            pd.DataFrame({"test": [1, 2, 3], "target": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3], "target": [3, 2, 1]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            False,
        ),
        (
            pd.DataFrame({"test": [1, 2, 3], "target": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3], "target": [3, 2, 1]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            False,
        ),
        (
            pd.DataFrame({"test": [1, 2, 3], "target": [1, 2, 3]}),
            pd.DataFrame({"test": [4, 5, 6], "target": [1, 2, 3]}),
            "target",
            DataDriftOptions(),
            ColumnType.Categorical,
            False,
        ),
    ),
)
def test_get_one_column_drift_success(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    options: DataDriftOptions,
    column_type: ColumnType,
    expected_drift_detected: bool,
):
    dataset_columns = process_columns(reference_data, ColumnMapping())
    result = get_one_column_drift(
        current_data=current_data,
        reference_data=reference_data,
        column_name=column_name,
        options=options,
        dataset_columns=dataset_columns,
        column_type=column_type,
        agg_data=False,
    )
    assert result.drift_detected == expected_drift_detected


@pytest.mark.parametrize(
    "current_data, reference_data, column_name, options, column_type, expected_value_error",
    (
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "feature",
            DataDriftOptions(),
            ColumnType.Categorical,
            "Cannot find column 'feature' in current dataset",
        ),
        (
            pd.DataFrame({"feature": [1, 2, 3]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "feature",
            DataDriftOptions(),
            ColumnType.Categorical,
            "Cannot find column 'feature' in reference dataset",
        ),
        (
            pd.DataFrame({"test": [None, None, None]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            "An empty column 'test' was provided for drift calculation in the current dataset.",
        ),
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"test": [None, None, None]}),
            "test",
            DataDriftOptions(),
            ColumnType.Categorical,
            "An empty column 'test' was provided for drift calculation in the reference dataset.",
        ),
        (
            pd.DataFrame({"test": ["a", 2, "c"]}),
            pd.DataFrame({"test": [1, 2, 3]}),
            "test",
            DataDriftOptions(),
            ColumnType.Numerical,
            "Column 'test' in current dataset should contain numerical values only.",
        ),
        (
            pd.DataFrame({"test": [1, 2, 3]}),
            pd.DataFrame({"test": ["a", "b", 3]}),
            "test",
            DataDriftOptions(),
            ColumnType.Numerical,
            "Column 'test' in reference dataset should contain numerical values only.",
        ),
    ),
)
def test_get_one_column_drift_value_error(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    options: DataDriftOptions,
    column_type: ColumnType,
    expected_value_error: bool,
):
    dataset_columns = process_columns(reference_data, ColumnMapping())
    with pytest.raises(ValueError) as error:
        get_one_column_drift(
            current_data=current_data,
            reference_data=reference_data,
            column_name=column_name,
            options=options,
            dataset_columns=dataset_columns,
            column_type=column_type,
            agg_data=False,
        )
    assert error.value.args[0] == expected_value_error


@pytest.mark.parametrize("stattest", ["wasserstein", "psi"])
def test_get_drift_for_columns_drops_inf_without_nan(stattest: str):
    reference_data = pd.DataFrame({"feature": [float(i) for i in range(50)]})
    current_data = pd.DataFrame({"feature": [float(i) for i in range(50)]})
    # an infinite value and no NaN in the column
    current_data.loc[0, "feature"] = np.inf
    dataset_columns = process_columns(reference_data, ColumnMapping(numerical_features=["feature"]))
    options = DataDriftOptions(all_features_stattest=stattest)

    result = get_drift_for_columns(
        current_data=current_data,
        reference_data=reference_data,
        dataset_columns=dataset_columns,
        data_drift_options=options,
        agg_data=True,
    )
    single_column = get_one_column_drift(
        current_data=current_data,
        reference_data=reference_data,
        column_name="feature",
        options=options,
        dataset_columns=dataset_columns,
        column_type=ColumnType.Numerical,
        agg_data=True,
    )

    drift = result.drift_by_columns["feature"]
    assert np.isfinite(drift.drift_score)
    assert drift.drift_score == pytest.approx(single_column.drift_score)
    assert not drift.drift_detected
