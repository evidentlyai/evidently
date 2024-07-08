import json
from typing import Any
from typing import Callable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from evidently._pydantic_compat import BaseModel
from evidently.base_metric import MetricResult
from evidently.core import BaseResult
from evidently.utils import NumpyEncoder


def iterate_obj_fields(
    obj: Any, paths: List[str], early_stop: Optional[Callable[[Any, List[str]], Optional[List[Tuple[str, Any]]]]] = None
) -> Iterator[Tuple[str, Any]]:
    if early_stop is not None:
        es = early_stop(obj, paths)
        if es is not None:
            yield from es
            return
    if isinstance(obj, list):
        return
    if isinstance(obj, dict):
        yield from (r for key, value in obj.items() for r in iterate_obj_fields(value, paths + [str(key)], early_stop))
        return
    if isinstance(obj, BaseResult) and obj.__config__.extract_as_obj:
        yield ".".join(paths), obj
        return
    if isinstance(obj, BaseModel):
        yield from (
            r
            for name, field in obj.__fields__.items()
            for r in iterate_obj_fields(getattr(obj, name), paths + [name], early_stop)
        )
        return
    yield ".".join(paths), obj


def iterate_obj_float_fields(obj: Any, paths: List[str]) -> Iterator[Tuple[str, str]]:
    for path, value in iterate_obj_fields(obj, paths):
        if isinstance(value, BaseResult) and value.__config__.extract_as_obj:
            yield path, json.dumps(value.dict(), cls=NumpyEncoder)
            continue
        try:
            value = str(float(value))
            yield path, value
        except (TypeError, ValueError):
            continue


def iterate_metric_results_fields(metric_result: MetricResult) -> Iterator[Tuple[str, str]]:
    yield from iterate_obj_float_fields(metric_result, [])
