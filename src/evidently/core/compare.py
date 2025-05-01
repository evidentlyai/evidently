from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import pandas as pd

from evidently.core.report import Snapshot

CompareIndex = Union[str, List[str], Callable[[Snapshot], Any]]


def _get_index(index: CompareIndex, run: Snapshot, i: int) -> Any:
    if isinstance(index, list):
        return index[i]
    if callable(index):
        return index(run)
    if index == "timestamp":
        return run._timestamp
    if index.startswith("metadata."):
        key = index[len("metadata.") :]
        return run._metadata[key]
    raise ValueError(f"Invalid index: {index}")


def compare(
    *runs: Snapshot, index: CompareIndex = "timestamp", all_metrics: bool = False, use_tests: bool = False
) -> pd.DataFrame:
    if isinstance(index, list) and len(index) != len(runs):
        raise ValueError("Index and runs must have same length")

    common_metrics = set.intersection(*[set(r._top_level_metrics) for r in runs])
    result: Dict[str, Dict[int, Union[float, str]]] = defaultdict(dict)
    for i, run in enumerate(runs):
        result["index"][i] = _get_index(index, run, i)
        for metric_id in run._top_level_metrics:
            if not all_metrics and metric_id not in common_metrics:
                continue
            metric_result = run._metrics[metric_id]
            if use_tests:
                for test in metric_result.tests:
                    result[test.name][i] = test.status.value
            else:
                for key, value in metric_result.itervalues():
                    col = f"{metric_result.display_name}.{key}"
                    result[col][i] = value
    return (
        pd.DataFrame({col: [val.get(i, None) for i in range(len(runs))] for col, val in result.items()})
        .set_index("index")
        .T
    )
