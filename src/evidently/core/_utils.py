import inspect
from typing import Iterable
from typing import List
from typing import Tuple


def not_implemented(self_obj: object):
    currentframe = inspect.currentframe()
    name = "(unknown)"
    if currentframe is not None and currentframe.f_back:
        name = currentframe.f_back.f_code.co_name
    return NotImplementedError(f"Metric Type: {type(self_obj)} should implement {name}()")


def _flatten(obj: object, paths: List[str] = None) -> Iterable[Tuple[str, float]]:
    paths = paths or []
    if isinstance(obj, float):
        yield ".".join(paths), obj
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _flatten(v, paths + [str(k)])
        return
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _flatten(v, paths + [str(i)])
        return
    raise NotImplementedError("Not implemented for {}".format(type(obj)))
