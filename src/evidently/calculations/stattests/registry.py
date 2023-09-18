import dataclasses
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd

from evidently.calculations import stattests
from evidently.core import ColumnType

StatTestFuncType = Callable[[pd.Series, pd.Series, ColumnType, float], Tuple[float, bool]]


@dataclasses.dataclass
class StatTestResult:
    drift_score: float
    drifted: bool
    actual_threshold: float


@dataclasses.dataclass
class StatTest:
    name: str
    display_name: str
    func: StatTestFuncType
    allowed_feature_types: List[ColumnType]
    default_threshold: float = 0.05

    def __call__(
        self, reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, threshold: Optional[float]
    ) -> StatTestResult:
        actual_threshold = self.default_threshold if threshold is None else threshold
        p = self.func(reference_data, current_data, feature_type, actual_threshold)
        drift_score, drifted = p
        return StatTestResult(drift_score=drift_score, drifted=drifted, actual_threshold=actual_threshold)

    def __hash__(self):
        # hash by name, so stattests with same name would be the same.
        return hash(self.name)


PossibleStatTestType = Union[str, StatTestFuncType, StatTest]

_registered_stat_tests: Dict[str, Dict[ColumnType, StatTest]] = {}
_registered_stat_test_funcs: Dict[StatTestFuncType, str] = {}


def register_stattest(stat_test: StatTest):
    _registered_stat_tests[stat_test.name] = {ft: stat_test for ft in stat_test.allowed_feature_types}
    _registered_stat_test_funcs[stat_test.func] = stat_test.name


def _get_default_stattest(reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType) -> StatTest:
    n_values = pd.concat([reference_data, current_data]).nunique()
    if feature_type == ColumnType.Text:
        if reference_data.shape[0] > 1000:
            return stattests.abs_text_content_drift_stat_test
        return stattests.perc_text_content_drift_stat_test
    elif reference_data.shape[0] <= 1000:
        if feature_type == ColumnType.Numerical:
            if n_values <= 5:
                return stattests.chi_stat_test if n_values > 2 else stattests.z_stat_test
            elif n_values > 5:
                return stattests.ks_stat_test
        elif feature_type == ColumnType.Categorical:
            return stattests.chi_stat_test if n_values > 2 else stattests.z_stat_test
    elif reference_data.shape[0] > 1000:
        if feature_type == ColumnType.Numerical:
            n_values = pd.concat([reference_data, current_data]).nunique()
            if n_values <= 5:
                return stattests.jensenshannon_stat_test
            elif n_values > 5:
                return stattests.wasserstein_stat_test
        elif feature_type == ColumnType.Categorical:
            return stattests.jensenshannon_stat_test
    raise ValueError(f"Unexpected feature_type {feature_type}")


def get_stattest(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: Union[ColumnType, str],
    stattest_func: Optional[PossibleStatTestType],
) -> StatTest:
    if isinstance(feature_type, str):
        feature_type = ColumnType(feature_type)
    if stattest_func is None:
        return _get_default_stattest(reference_data, current_data, feature_type)
    return get_registered_stattest(stattest_func, feature_type)


def get_registered_stattest(stattest_func: Optional[PossibleStatTestType], feature_type: ColumnType = None) -> StatTest:
    if isinstance(stattest_func, StatTest):
        return stattest_func
    if callable(stattest_func) and stattest_func not in _registered_stat_test_funcs:
        return StatTest(
            name="",
            display_name=f"custom function '{stattest_func.__name__}'",
            func=stattest_func,
            allowed_feature_types=[],
        )
    if callable(stattest_func) and stattest_func in _registered_stat_test_funcs:
        stattest_name = _registered_stat_test_funcs[stattest_func]
    elif isinstance(stattest_func, str):
        stattest_name = stattest_func
    else:
        raise ValueError(f"Unexpected type of stattest argument ({type(stattest_func)}), expected: str or Callable")
    funcs = _registered_stat_tests.get(stattest_name, None)
    if funcs is None or feature_type is None:
        raise StatTestNotFoundError(stattest_name)
    func = funcs.get(feature_type)
    if func is None:
        raise StatTestInvalidFeatureTypeError(stattest_name, feature_type)
    return func


def get_registered_stattest_name(stattest_func: Optional[PossibleStatTestType], feature_type: ColumnType = None) -> str:
    stattest_name = get_registered_stattest(stattest_func, feature_type).name
    if stattest_name:
        return stattest_name
    raise StatTestNotFoundError(f"No registered stattest for function {stattest_func}. Please register it")


class StatTestNotFoundError(ValueError):
    def __init__(self, stattest_name: str):
        super().__init__(
            f"No stattest found of name {stattest_name}. " f"Available stattests: {list(_registered_stat_tests.keys())}"
        )


class StatTestInvalidFeatureTypeError(ValueError):
    def __init__(self, stattest_name: str, feature_type: ColumnType):
        super().__init__(
            f"Stattest {stattest_name} isn't applicable to feature of type {feature_type.value}. "
            f"Available feature types: {list(_registered_stat_tests[stattest_name].keys())}"
        )
