from typing import Any
from typing import Iterator
from typing import List
from typing import Tuple

from evidently._pydantic_compat import BaseModel
from evidently.base_metric import MetricResult


def iterate_obj_fields(obj: Any, paths: List[str]) -> Iterator[Tuple[str, float]]:
    if isinstance(obj, list):
        return
    if isinstance(obj, dict):
        yield from (r for key, value in obj.items() for r in iterate_obj_fields(value, paths + [key]))
        return
    if isinstance(obj, BaseModel):
        yield from (
            r for name, field in obj.__fields__.items() for r in iterate_obj_fields(getattr(obj, name), paths + [name])
        )
        return
    try:
        value = float(obj)
        yield ".".join(paths), value
    except (TypeError, ValueError):
        return


def iterate_metric_results_fields(metric_result: MetricResult) -> Iterator[Tuple[str, float]]:
    yield from iterate_obj_fields(metric_result, [])
