import pandas as pd
import pytest

from evidently.core.datasets import BinaryClassification
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import Regression
from evidently.core.report import Report
from evidently.descriptors import TextLength
from evidently.legacy.utils.types import ApproxValue
from evidently.tests import Reference
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import gte
from evidently.tests import lt
from evidently.tests import lte


@pytest.fixture
def sample_dataset():
    data = pd.DataFrame(
        data={
            "column_1": [1, 2, 3, 4, -1, 5],
            "column_2": ["a", "aa", "aaaa", "aaaaaaa", None, "aa"],
            "text_column": ["a", "aa", "aaaa", "aaaaaaa", None, "aa"],
            "target": [1, 1, 0, 0, 1, 1],
            "prediction": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        }
    )

    definition = DataDefinition(
        numerical_columns=["column_1"],
        categorical_columns=["column_2"],
        text_columns=["text_column"],
        classification=[BinaryClassification()],
    )

    return Dataset.from_pandas(
        data,
        data_definition=definition,
        descriptors=[
            TextLength("column_2", alias="target2"),
            TextLength("column_2", alias="prediction2"),
        ],
    )


@pytest.fixture
def regression_sample_dataset():
    data = pd.DataFrame(
        data={
            "column_1": [1, 2, 3, 4, -1, 5],
            "column_2": ["a", "aa", "aaaa", "aaaaaaa", None, "aa"],
            "text_column": ["a", "aa", "aaaa", "aaaaaaa", None, "aa"],
            "target": [1, 1, 0, 0, 1, 1],
            "prediction": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        }
    )

    definition = DataDefinition(
        numerical_columns=["column_1", "target", "prediction"],
        categorical_columns=["column_2"],
        text_columns=["text_column"],
        regression=[Regression(target="target", prediction="prediction")],
    )

    return Dataset.from_pandas(
        data,
        data_definition=definition,
        descriptors=[
            TextLength("column_2", alias="target2"),
            TextLength("column_2", alias="prediction2"),
        ],
    )


# Classification Metrics Tests
def test_classification_metrics(sample_dataset):
    from evidently.metrics import FNR
    from evidently.metrics import FPR
    from evidently.metrics import TNR
    from evidently.metrics import TPR
    from evidently.metrics import Accuracy
    from evidently.metrics import F1Score
    from evidently.metrics import LogLoss
    from evidently.metrics import Precision
    from evidently.metrics import Recall
    from evidently.metrics import RocAuc

    report = Report(
        [
            F1Score(probas_threshold=0.4),
            Accuracy(probas_threshold=0.4),
            Precision(probas_threshold=0.4),
            Recall(probas_threshold=0.4),
            TPR(probas_threshold=0.4),
            TNR(probas_threshold=0.4),
            FPR(probas_threshold=0.4),
            FNR(probas_threshold=0.4),
            RocAuc(probas_threshold=0.4),
            LogLoss(probas_threshold=0.4),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_classification_by_label_metrics(sample_dataset):
    from evidently.metrics import F1ByLabel
    from evidently.metrics import PrecisionByLabel
    from evidently.metrics import RecallByLabel
    from evidently.metrics import RocAucByLabel

    report = Report(
        [
            F1ByLabel(probas_threshold=0.4, tests={0: [lte(0.2)]}),
            PrecisionByLabel(probas_threshold=0.4),
            RecallByLabel(probas_threshold=0.4),
            RocAucByLabel(probas_threshold=0.4),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_dummy_classification_metrics(sample_dataset):
    from evidently.metrics import DummyF1Score
    from evidently.metrics import DummyPrecision
    from evidently.metrics import DummyRecall

    report = Report(
        [
            DummyF1Score(probas_threshold=0.4),
            DummyPrecision(probas_threshold=0.4),
            DummyRecall(probas_threshold=0.4),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


# Column Statistics Tests
def test_column_statistics_metrics(sample_dataset):
    from evidently.metrics.column_statistics import MaxValue
    from evidently.metrics.column_statistics import MeanValue
    from evidently.metrics.column_statistics import MedianValue
    from evidently.metrics.column_statistics import MinValue
    from evidently.metrics.column_statistics import QuantileValue
    from evidently.metrics.column_statistics import StdValue

    report = Report(
        [
            MinValue(column="column_1", tests=[gte(0.2)]),
            MaxValue(column="column_1", tests=[gte(Reference(relative=0.1))]),
            MedianValue(column="column_1"),
            MeanValue(column="column_1"),
            StdValue(column="column_1"),
            QuantileValue(column="column_1"),
            QuantileValue(column="column_1", quantile=0.95),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


# Value Count Tests
def test_value_count_metrics(sample_dataset):
    from evidently.metrics import CategoryCount
    from evidently.metrics import InListValueCount
    from evidently.metrics import InRangeValueCount
    from evidently.metrics import MissingValueCount
    from evidently.metrics import OutListValueCount
    from evidently.metrics import OutRangeValueCount

    report = Report(
        [
            CategoryCount(
                column="column_2",
                category="a",
                tests=[
                    eq(1),
                    lte(2),
                    lte(Reference(relative=0.1)),
                    lte(Reference(absolute=1)),
                    gte(2),
                    lt(1),
                    gt(1),
                ],
                share_tests=[
                    lte(0.5),
                    eq(ApproxValue(0.19, absolute=0.015)),
                ],
            ),
            InRangeValueCount(column="column_1", left=1, right=3, count_tests=[lte(Reference(absolute=1))]),
            OutRangeValueCount(column="column_1", left=1, right=3),
            InListValueCount(column="column_2", values=["a", "aa"]),
            OutListValueCount(column="column_2", values=["a", "aa"]),
            MissingValueCount(column="column_2"),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


# Dataset Structure Tests
def test_dataset_structure_metrics(sample_dataset):
    from evidently.metrics import ColumnCount
    from evidently.metrics import DuplicatedRowCount
    from evidently.metrics import RowCount

    report = Report(
        [
            ColumnCount(),
            RowCount(),
            DuplicatedRowCount(),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


# Regression Metrics Tests
def test_regression_metrics(regression_sample_dataset):
    from evidently.metrics import MAE
    from evidently.metrics import MAPE
    from evidently.metrics import RMSE
    from evidently.metrics import AbsMaxError
    from evidently.metrics import MeanError
    from evidently.metrics import R2Score

    report = Report(
        [
            MeanError(),
            MAE(),
            MAPE(),
            RMSE(),
            R2Score(),
            AbsMaxError(),
        ]
    )

    snapshot = report.run(regression_sample_dataset, regression_sample_dataset)
    assert snapshot is not None


def test_dummy_regression_metrics(regression_sample_dataset):
    from evidently.metrics import DummyMAE
    from evidently.metrics import DummyMAPE
    from evidently.metrics import DummyRMSE

    report = Report(
        [
            DummyMAE(),
            DummyMAPE(),
            DummyRMSE(),
        ]
    )

    snapshot = report.run(regression_sample_dataset, regression_sample_dataset)
    assert snapshot is not None


# Preset Tests
def test_classification_presets(sample_dataset):
    from evidently.presets import ClassificationDummyQuality
    from evidently.presets import ClassificationQuality
    from evidently.presets import ClassificationQualityByLabel

    report = Report(
        [
            ClassificationQuality(),
            ClassificationDummyQuality(),
            ClassificationQualityByLabel(),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_data_drift_preset(sample_dataset):
    from evidently.presets import DataDriftPreset

    report = Report([DataDriftPreset()])
    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_value_stats_preset(sample_dataset):
    from evidently.presets import ValueStats

    report = Report(
        [
            ValueStats("column_1"),
            ValueStats("column_2"),
        ]
    )

    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_dataset_stats_preset(sample_dataset):
    from evidently.presets import DatasetStats

    report = Report([DatasetStats()])
    snapshot = report.run(sample_dataset, sample_dataset)
    assert snapshot is not None


def test_regression_preset(regression_sample_dataset):
    from evidently.presets import RegressionPreset

    report = Report([RegressionPreset()])
    snapshot = report.run(regression_sample_dataset, regression_sample_dataset)
    assert snapshot is not None
