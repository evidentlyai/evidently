from typing import List, Union, Callable, Tuple, Dict

REGISTERED_STAT_TEST: Dict[str, Dict[str, Callable]] = {}


def stattest(name: str, allowed_feature_types: List[str]):
    def wrapper(func):
        REGISTERED_STAT_TEST[name] = {feature_type: func for feature_type in allowed_feature_types}
        return func

    return wrapper


def get_stattest(stattest_func: Union[str, Callable], feature_type: str) -> Tuple[str, Callable]:
    if callable(stattest_func):
        return f"custom function {stattest_func.__name__}", stattest_func
    if isinstance(stattest_func, str):
        funcs = REGISTERED_STAT_TEST.get(stattest_func, None)
        if funcs is None:
            raise StatTestNotFoundError(stattest_func)
        func = funcs.get(feature_type)
        if func is None:
            raise StatTestInvalidFeatureTypeError(stattest_func, feature_type)
        return stattest_func, func
    raise ValueError(f"Unexpected type of stattest argument ({type(stattest_func)}), exptected: str or Callable")


class StatTestNotFoundError(ValueError):
    def __init__(self, stattest_name: str):
        super().__init__(f"No stattest found of name {stattest_name}. "
                         f"Available stattests: {list(REGISTERED_STAT_TEST.keys())}")


class StatTestInvalidFeatureTypeError(ValueError):
    def __init__(self, stattest_name: str, feature_type: str):
        super().__init__(f"Stattest {stattest_name} isn't applicable to feature of type {feature_type}. "
                         f"Available feature types: {list(REGISTERED_STAT_TEST[stattest_name].keys())}")
