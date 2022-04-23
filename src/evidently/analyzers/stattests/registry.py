from typing import List, Union, Callable, Tuple, Dict

import dataclasses

import pandas as pd


StatTestFuncType = Callable[[pd.Series, pd.Series, str, float], Tuple[float, bool]]


@dataclasses.dataclass
class StatTest:
    name: str
    display_name: str
    func: StatTestFuncType
    allowed_feature_types: List[str]


PossibleStatTestType = Union[str, StatTestFuncType, StatTest]

_registered_stat_tests: Dict[str, Dict[str, StatTest]] = {}
_registered_stat_test_funcs: Dict[StatTestFuncType, str] = {}


def register_stattest(stat_test: StatTest):
    _registered_stat_tests[stat_test.name] = {ft: stat_test for ft in stat_test.allowed_feature_types}
    _registered_stat_test_funcs[stat_test.func] = stat_test.name


def get_stattest(stattest_func: PossibleStatTestType, feature_type: str) -> StatTest:
    if isinstance(stattest_func, StatTest):
        return stattest_func
    if callable(stattest_func) and stattest_func not in _registered_stat_test_funcs:
        return StatTest(
            name="",
            display_name=f"custom function '{stattest_func.__name__}'",
            func=stattest_func,
            allowed_feature_types=[]
        )
    if callable(stattest_func) and stattest_func in _registered_stat_test_funcs:
        stattest_name = _registered_stat_test_funcs[stattest_func]
    elif isinstance(stattest_func, str):
        stattest_name = stattest_func
    else:
        raise ValueError(f"Unexpected type of stattest argument ({type(stattest_func)}), exptected: str or Callable")
    funcs = _registered_stat_tests.get(stattest_name, None)
    if funcs is None:
        raise StatTestNotFoundError(stattest_name)
    func = funcs.get(feature_type)
    if func is None:
        raise StatTestInvalidFeatureTypeError(stattest_name, feature_type)
    return func


class StatTestNotFoundError(ValueError):
    def __init__(self, stattest_name: str):
        super().__init__(f"No stattest found of name {stattest_name}. "
                         f"Available stattests: {list(_registered_stat_tests.keys())}")


class StatTestInvalidFeatureTypeError(ValueError):
    def __init__(self, stattest_name: str, feature_type: str):
        super().__init__(f"Stattest {stattest_name} isn't applicable to feature of type {feature_type}. "
                         f"Available feature types: {list(_registered_stat_tests[stattest_name].keys())}")
