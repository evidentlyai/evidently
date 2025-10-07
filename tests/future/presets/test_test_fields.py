import dataclasses
from inspect import isabstract
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_origin

import pandas as pd
import pytest

from evidently import BinaryClassification
from evidently import DataDefinition
from evidently import Dataset
from evidently._pydantic_compat import ModelField
from evidently.core.container import MetricContainer
from evidently.core.metric_types import MeanStdMetric
from evidently.core.metric_types import MeanStdMetricTests
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricTest
from evidently.core.metric_types import convert_tests
from evidently.core.report import Report
from evidently.core.tests import GenericTest
from evidently.descriptors import TextLength
from evidently.generators import ColumnMetricGenerator
from evidently.metrics import FNR
from evidently.metrics import FPR
from evidently.metrics import MAE
from evidently.metrics import MAPE
from evidently.metrics import RMSE
from evidently.metrics import TNR
from evidently.metrics import TPR
from evidently.metrics import AbsMaxError
from evidently.metrics import Accuracy
from evidently.metrics import AlmostConstantColumnsCount
from evidently.metrics import AlmostDuplicatedColumnsCount
from evidently.metrics import ColumnCorrelations
from evidently.metrics import ColumnCount
from evidently.metrics import ConstantColumnsCount
from evidently.metrics import DatasetCorrelations
from evidently.metrics import DatasetMissingValueCount
from evidently.metrics import DummyMAE
from evidently.metrics import DummyMAPE
from evidently.metrics import DummyRMSE
from evidently.metrics import DuplicatedColumnsCount
from evidently.metrics import DuplicatedRowCount
from evidently.metrics import EmptyColumnsCount
from evidently.metrics import EmptyRowsCount
from evidently.metrics import F1ByLabel
from evidently.metrics import F1Score
from evidently.metrics import LogLoss
from evidently.metrics import MaxValue
from evidently.metrics import MeanError
from evidently.metrics import MeanValue
from evidently.metrics import MinValue
from evidently.metrics import MissingValueCount
from evidently.metrics import Precision
from evidently.metrics import PrecisionByLabel
from evidently.metrics import QuantileValue
from evidently.metrics import R2Score
from evidently.metrics import Recall
from evidently.metrics import RecallByLabel
from evidently.metrics import RocAuc
from evidently.metrics import RocAucByLabel
from evidently.metrics import RowCount
from evidently.metrics import StdValue
from evidently.metrics import UniqueValueCount
from evidently.metrics.group_by import GroupBy
from evidently.metrics.row_test_summary import RowTestSummary
from evidently.presets import ClassificationDummyQuality
from evidently.presets import ClassificationPreset
from evidently.presets import ClassificationQuality
from evidently.presets import ClassificationQualityByLabel
from evidently.presets import DataDriftPreset
from evidently.presets import DatasetStats
from evidently.presets import DataSummaryPreset
from evidently.presets import RecsysPreset
from evidently.presets import RegressionDummyQuality
from evidently.presets import RegressionPreset
from evidently.presets import RegressionQuality
from evidently.presets import TextEvals
from evidently.presets.dataset_stats import ValueStatsTests
from evidently.presets.special import TestSummaryInfoPreset
from evidently.tests import eq
from tests.conftest import load_all_subtypes

load_all_subtypes(MetricContainer)


def mean_std_check(metric: MeanStdMetric, tests: MeanStdMetricTests):
    return metric.mean_tests == tests.mean and metric.std_tests == tests.std


value_stats_metric_mapping = {
    MissingValueCount: "missing_values_count_tests",
    MinValue: "min_tests",
    MaxValue: "max_tests",
    MeanValue: "mean_tests",
    RowCount: "row_count_tests",
    StdValue: "std_tests",
    UniqueValueCount: "unique_values_count_tests",
}


def value_stats_tests_check(metric: Metric, tests: Dict[str, ValueStatsTests]):
    ts = next(iter(tests.values())).convert()
    for metric_type, field_name in value_stats_metric_mapping.items():
        if not isinstance(metric, metric_type):
            continue
        return metric.tests == getattr(ts, field_name)
    if isinstance(metric, QuantileValue):
        return metric.tests == getattr(ts, f"q{int(metric.quantile * 100)}_tests")
    if isinstance(metric, RowTestSummary):
        return True
    raise ValueError(f"Unknown metric type {metric.__class__.__name__}")


FieldOrFieldCheck = Union[str, Callable[[Metric, Any], bool]]
MetricTypeOrMetricCheck = Union[Type[Metric], Callable[[Metric], bool]]
preset_types: Dict[Type[MetricContainer], Dict[str, Tuple[MetricTypeOrMetricCheck, FieldOrFieldCheck]]] = {
    ClassificationQuality: {
        "accuracy_tests": (Accuracy, "tests"),
        "precision_tests": (Precision, "tests"),
        "recall_tests": (Recall, "tests"),
        "f1score_tests": (F1Score, "tests"),
        "rocauc_tests": (RocAuc, "tests"),
        "logloss_tests": (LogLoss, "tests"),
        "tpr_tests": (TPR, "tests"),
        "tnr_tests": (TNR, "tests"),
        "fpr_tests": (FPR, "tests"),
        "fnr_tests": (FNR, "tests"),
    },
    ClassificationDummyQuality: {},
    ClassificationQualityByLabel: {
        "f1score_tests": (F1ByLabel, "tests"),
        "precision_tests": (PrecisionByLabel, "tests"),
        "recall_tests": (RecallByLabel, "tests"),
        "rocauc_tests": (RocAucByLabel, "tests"),
    },
    ClassificationPreset: {
        "accuracy_tests": (Accuracy, "tests"),
        "precision_tests": (Precision, "tests"),
        "recall_tests": (Recall, "tests"),
        "f1score_tests": (F1Score, "tests"),
        "rocauc_tests": (RocAuc, "tests"),
        "logloss_tests": (LogLoss, "tests"),
        "tpr_tests": (TPR, "tests"),
        "tnr_tests": (TNR, "tests"),
        "fpr_tests": (FPR, "tests"),
        "fnr_tests": (FNR, "tests"),
        "f1score_by_label_tests": (F1ByLabel, "tests"),
        "precision_by_label_tests": (PrecisionByLabel, "tests"),
        "recall_by_label_tests": (RecallByLabel, "tests"),
        "rocauc_by_label_tests": (RocAucByLabel, "tests"),
    },
    DataSummaryPreset: {
        "row_count_tests": (lambda m: isinstance(m, RowCount) and m.tests, "tests"),
        "column_count_tests": (lambda m: isinstance(m, ColumnCount) and m.tests, "tests"),  # todo: duplicated metrics
        "duplicated_row_count_tests": (DuplicatedRowCount, "tests"),
        "duplicated_column_count_tests": (DuplicatedColumnsCount, "tests"),
        "almost_duplicated_column_count_tests": (AlmostDuplicatedColumnsCount, "tests"),
        "almost_constant_column_count_tests": (AlmostConstantColumnsCount, "tests"),
        "empty_row_count_tests": (EmptyRowsCount, "tests"),
        "empty_column_count_tests": (EmptyColumnsCount, "tests"),
        "constant_columns_count_tests": (ConstantColumnsCount, "tests"),
        "dataset_missing_value_count_tests": (DatasetMissingValueCount, "tests"),
        "column_tests": (lambda x: isinstance(x, Metric) and x.tests, value_stats_tests_check),
    },
    GroupBy: {},
    DataDriftPreset: {},
    RegressionPreset: {
        "mean_error_tests": (MeanError, mean_std_check),
        "mape_tests": (MAPE, mean_std_check),
        "rmse_tests": (RMSE, "tests"),
        "mae_tests": (MAE, mean_std_check),
        "r2score_tests": (R2Score, "tests"),
        "abs_max_error_tests": (AbsMaxError, "tests"),
    },
    TextEvals: {
        "row_count_tests": (lambda x: isinstance(x, RowCount) and x.tests, "tests"),
        # because of  duplicated RowCount metric in text evals
        "column_tests": (lambda x: not isinstance(x, RowCount) or x.tests, value_stats_tests_check),
    },
    RegressionDummyQuality: {
        "mae_tests": (DummyMAE, "tests"),
        "mape_tests": (DummyMAPE, "tests"),
        "rmse_tests": (DummyRMSE, "tests"),
    },
    ColumnMetricGenerator: {},
    DatasetStats: {
        "row_count_tests": (RowCount, "tests"),
        "column_count_tests": (lambda metric: isinstance(metric, ColumnCount) and metric.column_type is None, "tests"),
        "duplicated_row_count_tests": (DuplicatedRowCount, "tests"),
        "duplicated_column_count_tests": (DuplicatedColumnsCount, "tests"),
        "almost_duplicated_column_count_tests": (AlmostDuplicatedColumnsCount, "tests"),
        "almost_constant_column_count_tests": (AlmostConstantColumnsCount, "tests"),
        "empty_row_count_tests": (EmptyRowsCount, "tests"),
        "empty_column_count_tests": (EmptyColumnsCount, "tests"),
        "constant_columns_count_tests": (ConstantColumnsCount, "tests"),
        "dataset_missing_value_count_tests": (DatasetMissingValueCount, "tests"),
        "dataset_missing_value_share_tests": (DatasetMissingValueCount, "share_tests"),
    },
    RegressionQuality: {
        "mean_error_tests": (MeanError, mean_std_check),
        "mape_tests": (MAPE, mean_std_check),
        "rmse_tests": (RMSE, "tests"),
        "mae_tests": (MAE, mean_std_check),
        "r2score_tests": (R2Score, "tests"),
        "abs_max_error_tests": (AbsMaxError, "tests"),
    },
    RowTestSummary: {},
    TestSummaryInfoPreset: {},
    DatasetCorrelations: {},
    ColumnCorrelations: {},
    RecsysPreset: {},
}


def test_all_presets_tested():
    tested_types_set = set(preset_types)
    all_preset_types = set(s for s in MetricContainer.__subclasses__() if not isabstract(s))

    missing_test_fields: Dict[Type[MetricContainer], List[str]] = {}
    for preset_type in all_preset_types:
        all_test_fields = [tf[0] for tf in iter_type_test_fields(preset_type)]
        if preset_type not in tested_types_set:
            missing_test_fields[preset_type] = all_test_fields
            continue
        tested_fields = set(preset_types[preset_type])
        if tested_fields != set(all_test_fields):
            missing_test_fields[preset_type] = list(tested_fields - set(all_test_fields))

    def guess_metric_name(s):
        s = s.split("_tests")[0]
        return s.split("_")[0].capitalize() + "".join(w.title() for w in s.split("_")[1:])

    def _fmt(fields):
        return ", ".join(f"'{f}': ({guess_metric_name(f)}, 'tests')" for f in fields)

    format_missing = ", ".join(f"{t.__name__}: {{{_fmt(fs)}" f"}}" for t, fs in missing_test_fields.items())
    assert len(missing_test_fields) == 0, "Missing tests for preset fields: {}".format(format_missing)


def _is_test_field(field: ModelField) -> bool:
    if field.outer_type_ is bool:
        return False
    return "tests" in field.name


def _get_test_field_instance(
    field: ModelField, check: Union[GenericTest, MetricTest], preset_type: Type[MetricContainer]
):
    if get_origin(field.outer_type_) == dict:
        if field.type_ is ValueStatsTests:
            col = "text_length"
            return {
                col: ValueStatsTests(
                    unique_values_count_tests={"b": [check]},
                    **{
                        f.name: [check]
                        for f in dataclasses.fields(ValueStatsTests)
                        if f.name != "unique_values_count_tests"
                    },
                )
            }
        return {"a": [check]}
    if get_origin(field.outer_type_) == list:
        return [check]
    if field.outer_type_ is MeanStdMetricTests:
        return MeanStdMetricTests(mean=[check], std=[check])
    return NotImplementedError(f"Not implemented for {field.outer_type_}")


def iter_type_test_fields(preset_type: Type[MetricContainer]) -> Iterable[Tuple[str, ModelField]]:
    for field_name, field in preset_type.__fields__.items():
        if not _is_test_field(field):
            continue
        yield field_name, field


@pytest.mark.parametrize("preset_type", preset_types)
@pytest.mark.parametrize("check", [eq(0)])
def test_preset_type_test_fields(preset_type: Type[MetricContainer], check: Union[GenericTest, MetricTest]):
    errors = {}

    for field_name, field in iter_type_test_fields(preset_type):
        field_instance = _get_test_field_instance(field, check, preset_type)
        try:
            instance = preset_type(**{field_name: field_instance})
        except Exception as e:
            errors[field_name] = e
            continue
        dataset = Dataset.from_pandas(
            pd.DataFrame({"a": [1], "b": ["b"]}),
            data_definition=DataDefinition(classification=[BinaryClassification()]),
            descriptors=[TextLength("b")],
        )
        run = Report([]).run(dataset)
        gen_metrics = instance.generate_metrics(run._context)
        assert (
            field_name in preset_types[preset_type]
        ), f"Missing target for {preset_type.__name__}.{field_name}: available {[m.__class__.__name__ for m in gen_metrics]}"
        target_metric, field_check = preset_types[preset_type][field_name]
        metrics = [
            m
            for m in gen_metrics
            if (isinstance(target_metric, type) and isinstance(m, target_metric))
            or (not isinstance(target_metric, type) and target_metric(m))
        ]
        assert (
            len(metrics) != 0
        ), f"Could not determine target metric for {preset_type.__name__}.{field_name}: {gen_metrics}"
        for metric in metrics:
            if callable(field_check):
                assert field_check(
                    metric, field_instance
                ), f"Failed for {preset_type.__name__}.{field_name} with {metric}"
            else:
                assert getattr(metric, field_check) == convert_tests(field_instance), (
                    f"Failed for {preset_type.__name__}.{field_name} {metric.__class__.__name__}:"
                    f" {getattr(metric, field_check)} != {field_instance}"
                )
    assert len(errors) == 0, f"Failed for {preset_type.__name__}: {errors}"
