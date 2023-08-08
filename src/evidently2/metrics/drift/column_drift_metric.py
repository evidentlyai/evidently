import dataclasses
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import chisquare

from evidently2.core.calculation import CI
from evidently2.core.calculation import CR
from evidently2.core.calculation import Calculation
from evidently2.core.calculation import InputColumnData
from evidently2.core.calculation import InputData
from evidently2.core.calculation import InputValue
from evidently2.core.calculation import _CalculationBase
from evidently2.core.metric import ColumnMetricResultCalculation
from evidently2.core.metric import Metric
from evidently.base_metric import ColumnMetricResult
from evidently.base_metric import ColumnName
from evidently.base_metric import ColumnNotFound
from evidently.core import ColumnType
from evidently.metric_results import Distribution
from evidently.options import DataDriftOptions
from evidently.utils.data_preprocessing import DataDefinition


class ColumnDriftResult(ColumnMetricResult):
    stattest_name: str
    stattest_threshold: Optional[float]
    drift_score: float
    drift_detected: bool

    current_small_distribution: Distribution
    reference_small_distribution: Optional[Distribution]


# todo: generate dynamically?
class ColumnDriftResultCalculation(ColumnMetricResultCalculation[ColumnDriftResult]):
    stattest_name: str
    stattest_threshold: Optional[float]
    drift_score: Calculation
    drift_detected: Calculation

    current_small_distribution: Calculation
    reference_small_distribution: Calculation


class ColumnDriftMetric(Metric[ColumnDriftResult]):
    """Calculate drift metric for a column"""

    column_name: ColumnName
    stattest: Optional[str]
    stattest_threshold: Optional[float]

    def calculate(self, data: InputData) -> ColumnDriftResultCalculation:
        try:
            current_feature_data = data.get_current_column(self.column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in current dataset")
        try:
            reference_feature_data = data.get_reference_column(self.column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in reference dataset")

        column_type = ColumnType.Numerical
        if self.column_name.is_main_dataset():
            column_type = data.data_definition.get_column(self.column_name.name).column_type
        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)
        drift_result = get_one_column_drift(
            current_feature_data=current_feature_data,
            reference_feature_data=reference_feature_data,
            column=self.column_name,
            column_type=column_type,
            options=options,
            data_definition=data.data_definition,
        )

        return drift_result


class CleanColumn(Calculation[pd.Series, pd.Series]):
    def calculate(self, data: pd.Series) -> pd.Series:
        return data.replace([-np.inf, np.inf], np.nan).dropna()

    @property
    def empty(self):
        # todo: can we do this lazy?
        return self.get_result().empty


@dataclasses.dataclass
class StatTestResult:
    drift_score: Calculation
    drifted: Calculation
    actual_threshold: float


StatTestFuncType = Callable[[Calculation, Calculation, str, float], Tuple[Calculation, Calculation]]


@dataclasses.dataclass
class StatTest:
    name: str
    display_name: str
    func: StatTestFuncType
    allowed_feature_types: List[str]
    default_threshold: float = 0.05

    def __call__(
        self, reference_data: Calculation, current_data: Calculation, feature_type: str, threshold: Optional[float]
    ) -> StatTestResult:
        actual_threshold = self.default_threshold if threshold is None else threshold
        p = self.func(reference_data, current_data, feature_type, actual_threshold)
        drift_score, drifted = p
        return StatTestResult(drift_score=drift_score, drifted=drifted, actual_threshold=actual_threshold)

    def __hash__(self):
        # hash by name, so stattests with same name would be the same.
        return hash(self.name)


class DropNA(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.dropna()


class Unique(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.unique()


class CreateSet(Calculation):
    def calculate(self, data: CI) -> CR:
        return set(data)


class UnionList(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return list(data | self.second.get_result())


def get_unique_not_nan_values_list_from_series(current_data: Calculation, reference_data: Calculation) -> Calculation:
    """Get unique values from current and reference series, drop NaNs"""
    return UnionList(
        input_data=CreateSet(input_data=Unique(input_data=DropNA(input_data=current_data))),
        second=CreateSet(input_data=Unique(input_data=DropNA(input_data=reference_data))),
    )
    # return list(set(reference_data.dropna().unique()) | set(current_data.dropna().unique()))


class Size(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.shape[0]


class Div(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return data / self.second.get_result()


class ValueCounts(Calculation):
    def calculate(self, data: CI) -> CR:
        return data.value_counts()


class Mul(Calculation):
    second: Calculation

    def calculate(self, data: CI) -> CR:
        return data * self.second.get_result()


class MultDict(Calculation):
    mul: Calculation

    def calculate(self, data: CI) -> CR:
        m = self.mul.get_result()
        return {k: v * m for k, v in data.items()}


class ChiSquare(Calculation):
    exp: Calculation

    def calculate(self, data: CI) -> CR:
        exp = self.exp.get_result()
        keys = set(data.keys()) | set(exp.keys())
        return chisquare([data.get(k, 0) for k in keys], [exp.get(k, 0) for k in keys])[1]


class LessThen(Calculation):
    second: _CalculationBase

    def calculate(self, data: CI) -> CR:
        return data < self.second.get_result()


def _chi_stat_test(
    reference_data: Calculation, current_data: Calculation, feature_type: str, threshold: float
) -> Tuple[Calculation, Calculation]:
    # keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
    # k_norm = current_data.shape[0] / reference_data.shape[0]
    k_norm = Div(input_data=Size(input_data=current_data), second=Size(input_data=reference_data))
    ref_feature_dict = ValueCounts(input_data=reference_data)
    current_feature_dict = ValueCounts(input_data=current_data)
    f_exp = MultDict(input_data=ref_feature_dict, mul=k_norm)
    p_value = ChiSquare(input_data=current_feature_dict, exp=f_exp)
    # return p_value, p_value < threshold
    return p_value, LessThen(input_data=p_value, second=InputValue(data=threshold))


chi_stat_test = StatTest(
    name="chisquare", display_name="chi-square p_value", func=_chi_stat_test, allowed_feature_types=["cat"]
)

z_stat_test = wasserstein_stat_test = ks_stat_test = jensenshannon_stat_test = chi_stat_test


def _get_default_stattest(reference_data: pd.Series, feature_type: str) -> StatTest:
    if feature_type != "num":
        raise NotImplementedError

    # todo: we can make this lazy too
    n_values = reference_data.nunique()
    if reference_data.shape[0] <= 1000:
        if n_values <= 5:
            return chi_stat_test if n_values > 2 else z_stat_test
        elif n_values > 5:
            return ks_stat_test
    elif reference_data.shape[0] > 1000:
        if n_values <= 5:
            return jensenshannon_stat_test
        elif n_values > 5:
            return wasserstein_stat_test

    raise ValueError(f"Unexpected feature_type {feature_type}")


def get_stattest(reference_data: Calculation, feature_type: str, stattest_func: Optional[str]) -> StatTest:
    if stattest_func is None:
        return _get_default_stattest(reference_data.get_result(), feature_type)


class Histogram(Calculation[pd.Series, Distribution]):
    bins: int
    density: bool

    def __init__(self, input_data: _CalculationBase, bins: int, density: bool):
        super().__init__(input_data=input_data, bins=bins, density=density)

    def calculate(self, data: pd.Series) -> Distribution:
        y, x = [
            t.tolist()
            for t in np.histogram(
                data,
                bins=self.bins,
                density=self.density,
            )
        ]
        return Distribution(x=x, y=y)


class Mask(Calculation[pd.Series, pd.Series]):
    mask: Calculation

    def __init__(self, input_data: _CalculationBase, mask: Calculation):
        super().__init__(input_data=input_data, mask=mask)

    def calculate(self, data: CI) -> CR:
        return data[self.mask.get_result()]


class IsFinite(Calculation[pd.Series, pd.Series]):
    def __init__(self, input_data: _CalculationBase):
        super().__init__(input_data=input_data)

    def calculate(self, data: CI) -> CR:
        return np.isfinite(data)


def get_one_column_drift(
    *,
    current_feature_data: InputColumnData,
    reference_feature_data: InputColumnData,
    column: ColumnName,
    options: DataDriftOptions,
    data_definition: DataDefinition,
    column_type: ColumnType,
) -> ColumnDriftResultCalculation:
    if column_type not in (ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text):
        raise ValueError(f"Cannot calculate drift metric for column '{column}' with type {column_type}")

    target = data_definition.get_target_column()
    stattest = None
    threshold = None
    if column.is_main_dataset():
        if target and column.name == target.column_name and column_type == ColumnType.Numerical:
            stattest = options.num_target_stattest_func

        elif target and column.name == target.column_name and column_type == ColumnType.Categorical:
            stattest = options.cat_target_stattest_func

        if not stattest:
            stattest = options.get_feature_stattest_func(column.name, column_type.value)

        threshold = options.get_threshold(column.name, column_type.value)
    current_column = current_feature_data
    reference_column = reference_feature_data

    # clean and check the column in reference dataset
    reference_column = CleanColumn(
        input_data=reference_column
    )  # reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(
            f"An empty column '{column.name}' was provided for drift calculation in the reference dataset."
        )

    # clean and check the column in current dataset
    current_column = CleanColumn(
        input_data=current_column
    )  # current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"An empty column '{column.name}' was provided for drift calculation in the current dataset.")

    current_small_distribution = None
    reference_small_distribution = None

    # if column_type == ColumnType.Numerical:
    #     if not pd.api.types.is_numeric_dtype(reference_column):
    #         raise ValueError(f"Column '{column}' in reference dataset should contain numerical values only.")
    #
    #     if not pd.api.types.is_numeric_dtype(current_column):
    #         raise ValueError(f"Column '{column}' in current dataset should contain numerical values only.")

    drift_test_function = get_stattest(reference_column, column_type.value, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type.value, threshold)

    if column_type == ColumnType.Numerical:
        current_nbinsx = options.get_nbinsx(column.name)

        current_small_distribution = Histogram(
            Mask(current_column, IsFinite(current_column)), bins=current_nbinsx, density=True
        )
        reference_small_distribution = Histogram(
            Mask(reference_column, IsFinite(reference_column)), bins=current_nbinsx, density=True
        )

    metrics = ColumnDriftResultCalculation(
        column_name=column.name,
        column_type=column_type.name,
        stattest_name=drift_test_function.display_name,
        stattest_threshold=drift_result.actual_threshold,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        current_small_distribution=current_small_distribution,
        reference_small_distribution=reference_small_distribution,
    )

    return metrics
