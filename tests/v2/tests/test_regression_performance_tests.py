import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestValueMAE
from evidently.v2.tests import TestValueMAPE
from evidently.v2.tests import TestValueMeanError
from evidently.v2.tests import TestValueAbsMaxError
from evidently.v2.tests import TestValueRMSE
from evidently.v2.tests import TestValueR2Score
from evidently.v2.test_suite import TestSuite


def test_value_mae_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAE(gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMAE(eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_value_mape_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAPE(lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMAPE(eq=100)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_value_mean_error_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMeanError(gt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMeanError(eq=0.0)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_abs_max_error_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1, 2, 3, 4],
        }
    )
    suite = TestSuite(tests=[TestValueAbsMaxError(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite


def test_r2_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueR2Score(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite


def test_rmse_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueRMSE(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite
