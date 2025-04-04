import json
from typing import Any
from typing import Callable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from evidently._pydantic_compat import BaseModel
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import BaseResult
from evidently.legacy.utils import NumpyEncoder


def iterate_obj_fields(
    obj: Any, paths: List[str], early_stop: Optional[Callable[[Any, List[str]], Optional[List[Tuple[str, Any]]]]] = None
) -> Iterator[Tuple[str, Any]]:
    if early_stop is not None:
        es = early_stop(obj, paths)
        if es is not None:
            yield from es
            return

    from evidently.ui.backport import ByLabelCountValueV1
    from evidently.ui.backport import ByLabelValueV1

    if isinstance(obj, ByLabelValueV1):
        yield from (
            [(".".join(paths + ["values"]), obj.values)]
            + [(".".join(paths + ["values", str(key)]), str(val)) for key, val in obj.values.items()]
        )
        return
    if isinstance(obj, ByLabelCountValueV1):
        yield from (
            [(".".join(paths + ["counts"]), obj.counts)]
            + [(".".join(paths + ["counts", str(key)]), str(val)) for key, val in obj.counts.items()]
            + [(".".join(paths + ["shares"]), obj.shares)]
            + [(".".join(paths + ["shares", str(key)]), str(val)) for key, val in obj.shares.items()]
        )
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
        if isinstance(value, dict):
            yield path, json.dumps(value, cls=NumpyEncoder)
            continue
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
