import dataclasses
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

import numpy as np
import pandas as pd
from scipy.stats import chisquare

from evidently2.core.calculation import DataType
from evidently2.metrics.drift.column_drift_metric import ColumnDriftResult
from evidently2.metrics.drift.column_drift_metric import StatTest
from evidently.base_metric import ColumnName
from evidently.base_metric import MetricResult
from evidently.core import ColumnType
from evidently.metric_results import DistributionIncluded
from evidently.options import DataDriftOptions
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition

ReferenceResultType = TypeVar("ReferenceResultType", bound=MetricResult)
ResultType = TypeVar("ResultType", bound=MetricResult)

ColumnDataType = pd.Series


class Metric3(EvidentlyBaseModel, Generic[ReferenceResultType, ResultType]):
    def calculate_reference(self, data_definition: DataDefinition, reference: DataType) -> ReferenceResultType:
        raise NotImplementedError

    def calculate(self, data_definition: DataDefinition, ref: ReferenceResultType, current: DataType) -> ResultType:
        raise NotImplementedError


class StatTestReferenceResult(MetricResult):
    pass


class ChiSquareReferenceResult(StatTestReferenceResult):
    value_counts: Dict[Any, int]
    size: int


class ColumnDriftReferenceResult(MetricResult):
    stat_test: str
    stat_test_result: StatTestReferenceResult
    small_hist: Optional[DistributionIncluded]


@dataclasses.dataclass
class StatTestResult:
    drift_score: float
    drifted: bool
    actual_threshold: float


StatTestFuncType = Callable[[StatTestReferenceResult, ColumnDataType, str, float], Tuple[float, bool]]
StatTestReferenceFuncType = Callable[[ColumnDataType, str, float], StatTestReferenceResult]


@dataclasses.dataclass
class StatTest:
    name: str
    display_name: str
    func: StatTestFuncType
    get_reference: StatTestReferenceFuncType
    allowed_feature_types: List[str]
    default_threshold: float = 0.05

    def __call__(
        self,
        reference_data: StatTestReferenceResult,
        current_data: ColumnDataType,
        feature_type: str,
        threshold: Optional[float],
    ) -> StatTestResult:
        actual_threshold = self.default_threshold if threshold is None else threshold
        p = self.func(reference_data, current_data, feature_type, actual_threshold)
        drift_score, drifted = p
        return StatTestResult(drift_score=drift_score, drifted=drifted, actual_threshold=actual_threshold)

    def __hash__(self):
        # hash by name, so stattests with same name would be the same.
        return hash(self.name)


def _chi_stat_reference(
    reference_data: ColumnDataType, feature_type: str, threshold: float
) -> ChiSquareReferenceResult:
    return ChiSquareReferenceResult(value_counts=reference_data.value_counts().to_dict(), size=reference_data.shape[0])


def _chi_stat_test(
    reference_data: ChiSquareReferenceResult, current_data: ColumnDataType, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    k_norm = current_data.shape[0] / reference_data.size
    ref_feature_dict = reference_data.value_counts
    current_feature_dict = current_data.value_counts().to_dict()

    keys = set(ref_feature_dict.keys()) | set(current_feature_dict.keys())
    f_exp = [ref_feature_dict.get(key, 0) * k_norm for key in keys]
    f_obs = [current_feature_dict.get(key, 0) for key in keys]
    p_value = chisquare(f_obs, f_exp)[1]
    return p_value, p_value < threshold


chi_stat_test = StatTest(
    name="chisquare",
    display_name="chi-square p_value",
    func=_chi_stat_test,
    get_reference=_chi_stat_reference,
    allowed_feature_types=["cat"],
)

z_stat_test = wasserstein_stat_test = ks_stat_test = jensenshannon_stat_test = chi_stat_test


def _get_default_stattest(reference_data: ColumnDataType, feature_type: str) -> StatTest:
    if feature_type != "num":
        raise NotImplementedError

    # todo: we can make this lazy too
    n_values = reference_data.nunique()
    size = reference_data.shape[0]
    if size <= 1000:
        if n_values <= 5:
            return chi_stat_test if n_values > 2 else z_stat_test
        elif n_values > 5:
            return ks_stat_test
    elif size > 1000:
        if n_values <= 5:
            return jensenshannon_stat_test
        elif n_values > 5:
            return wasserstein_stat_test

    raise ValueError(f"Unexpected feature_type {feature_type}")


def get_stattest(reference_data: ColumnDataType, feature_type: str, stattest_func: Optional[str]) -> StatTest:
    if stattest_func is None:
        return _get_default_stattest(reference_data, feature_type)


class ColumnDriftMetric(Metric3[ColumnDriftReferenceResult, ColumnDriftResult]):
    column_name: ColumnName
    stattest: Optional[str]
    stattest_threshold: Optional[float]

    def calculate_reference(self, data_definition: DataDefinition, reference: DataType) -> ColumnDriftReferenceResult:
        column = self.column_name
        reference_column = reference[self.column_name.name]
        reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

        if reference_column.empty:
            raise ValueError(
                f"An empty column '{column.name}' was provided for drift calculation in the reference dataset."
            )

        column_type = data_definition.get_column(self.column_name.name).column_type
        stat_test = get_stattest(reference_column, column_type.value, self.stattest)

        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)

        reference_small_distribution = [
            t.tolist()
            for t in np.histogram(
                reference_column[np.isfinite(reference_column)],
                bins=options.get_nbinsx(self.column_name.name),
                density=True,
            )
        ]
        return ColumnDriftReferenceResult(
            stat_test=stat_test.name,
            stat_test_result=stat_test.get_reference(reference_column, column_type.value, self.stattest_threshold),
            small_hist=DistributionIncluded(x=reference_small_distribution[1], y=reference_small_distribution[0])
            if reference_small_distribution
            else None,
        )

    def calculate(
        self, data_definition: DataDefinition, ref: ColumnDriftReferenceResult, current: DataType
    ) -> ColumnDriftResult:
        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)

        # todo: get it from registry useing ref.stat_test
        drift_test_function = chi_stat_test
        assert drift_test_function.name == ref.stat_test

        column_type = data_definition.get_column(self.column_name.name).column_type

        current_column = current[self.column_name.name]
        current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()
        drift_result = drift_test_function(
            ref.stat_test_result, current_column, column_type.value, self.stattest_threshold
        )
        column = self.column_name

        current_small_distribution: Optional[List[List[float]]] = None

        if column_type == ColumnType.Numerical:
            current_nbinsx = options.get_nbinsx(column.name)

            current_small_distribution = [
                t.tolist()
                for t in np.histogram(
                    current_column[np.isfinite(current_column)],
                    bins=current_nbinsx,
                    density=True,
                )
            ]

        return ColumnDriftResult(
            column_name=column.name,
            column_type=column_type.name,
            stattest_name=drift_test_function.display_name,
            stattest_threshold=drift_result.actual_threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drifted,
            current_small_distribution=DistributionIncluded(
                x=current_small_distribution[1], y=current_small_distribution[0]
            )
            if current_small_distribution
            else None,
            reference_small_distribution=ref.small_hist,
        )
