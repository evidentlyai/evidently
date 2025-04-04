import dataclasses
from importlib import import_module
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from _pytest.mark import Mark
from _pytest.mark import ParameterSet
from _pytest.python import Metafunc

from evidently.legacy.base_metric import Metric
from tests.multitest.conftest import TestOutcome
from tests.multitest.datasets import DatasetTags
from tests.multitest.datasets import TestDataset
from tests.multitest.datasets import dataset_fixtures

OutcomeKeyType = Union[str, DatasetTags]
OutcomeKey = Tuple[OutcomeKeyType, ...]

REFRESH_FINGERPRINT_VALUES = False
_code_cache: Dict[str, List[str]] = {}

if hasattr(dataclasses, "KW_ONLY"):
    dec = dataclasses.dataclass(kw_only=True)
else:
    dec = dataclasses.dataclass()


@dec
class TestMetric:
    name: str
    metric: Metric
    fingerprint: str
    outcomes: Union[TestOutcome, Dict[Union[str, OutcomeKey, TestDataset], TestOutcome]]

    include_tags: List[DatasetTags] = dataclasses.field(default_factory=list)
    """Only run on datasets with all tags"""
    exclude_tags: List[DatasetTags] = dataclasses.field(default_factory=list)
    """Exclude datasets with any of theese tags"""

    dataset_names: Optional[List[str]] = None
    """Only run on datasets with any theese names"""
    datasets: Optional[List[TestDataset]] = None
    """Only run on those datasets"""

    marks: List[Mark] = dataclasses.field(default_factory=list)
    # additional_check: Optional[Callable[[Report], None]] = None
    # """Additional callable to call on report"""

    if REFRESH_FINGERPRINT_VALUES:

        def __post_init__(self):
            import inspect

            fingerprint = self.metric.get_fingerprint()
            if self.fingerprint is None or self.fingerprint != fingerprint:
                stack = inspect.stack()
                init_call = stack[2]
                if init_call.filename not in _code_cache:
                    with open(init_call.filename, "r", encoding="utf8") as f:
                        _code_cache[init_call.filename] = list(f.readlines())

                lines = _code_cache[init_call.filename]
                if self.fingerprint is None:
                    lineno = init_call.lineno - 1
                    line = lines[lineno]
                    if "TestMetric(" not in line:
                        raise Exception(f"Cannot find TestMetric init in line {line}")
                    lines[lineno] = line.replace("TestMetric(", f'TestMetric(\nfingerprint="{fingerprint}",')
                if self.fingerprint is not None and self.fingerprint != fingerprint:
                    template = f'fingerprint="{self.fingerprint}"'
                    for i, line in list(enumerate(lines)):
                        if template in line:
                            lines[i] = line.replace(template, f'fingerprint="{fingerprint}"')
                            break
                    else:
                        raise Exception(f"Cound not find line with {template}")
                with open(init_call.filename, "w", encoding="utf8") as f:
                    f.write("".join(lines))

    def get_outcome(self, dataset: TestDataset) -> TestOutcome:
        if isinstance(self.outcomes, TestOutcome):
            # single outcome
            return self.outcomes

        # get all valid keys as (dataset_name or None, set of tags)
        outcomes: List[Tuple[Tuple[Optional[str], Set[DatasetTags]], TestOutcome]] = []
        for key in self.outcomes:
            if isinstance(key, str):
                # if key is not tuple, its dataset name
                if key == dataset.name:
                    outcomes.append(((key, set()), self.outcomes[key]))
                continue
            # key is tuple, it's first value may be dataset name
            dataset_name: Optional[str] = None
            tags_set = set(key)
            if isinstance(key[0], str):
                dataset_name = key[0]
                tags_set = set(key[1:])
            if dataset_name is not None and dataset_name != dataset.name:
                continue
            if tags_set.issubset(dataset.tags):
                outcomes.append(((dataset_name, tags_set), self.outcomes[key]))

        if any(k[0] is not None for k, _ in outcomes):
            # we have at least one dataset name, so skip tags-only keys
            outcomes = [(k, v) for k, v in outcomes if k[0] is not None]

        if len(outcomes) == 0:
            raise ValueError(f"Can't find test outcome for {self.name} x {dataset.name}")

        # get longest tags match
        return list(sorted(outcomes, key=lambda x: -len(x[0][1])))[0][1]


metric_fixtures = []


def metric(f):
    m = f()
    if isinstance(m, list):
        metric_fixtures.extend(m)
    else:
        metric_fixtures.append(m)
    return f


def generate_dataset_outcome(m: TestMetric):
    if isinstance(m.outcomes, dict) and any(isinstance(k, TestDataset) for k in m.outcomes):
        if not all(isinstance(k, TestDataset) for k in m.outcomes):
            raise ValueError(f"All keys should be TestDataset if one is in {m.name}")
        yield from ((m, i, d, o) for i, (d, o) in enumerate(m.outcomes.items()))
        return
    if m.datasets is not None:
        yield from ((m, i, d, m.get_outcome(d)) for i, d in enumerate(m.datasets))
        return
    if m.dataset_names is not None:
        yield from ((m, i, d, m.get_outcome(d)) for i, d in enumerate(dataset_fixtures) if d.name in m.dataset_names)
        return

    for i, d in enumerate(dataset_fixtures):
        is_included = m.include_tags == [] or all(t in d.tags for t in m.include_tags)
        is_excluded = any(t in m.exclude_tags for t in d.tags)
        if is_included and not is_excluded:
            yield (
                m,
                i,
                d,
                m.get_outcome(d),
            )


def load_test_metrics():
    for module in ["classification", "data_integrity", "data_drift", "data_quality", "recsys", "regression", "custom"]:
        import_module(f"tests.multitest.metrics.{module}")


# for debugging
metric_type_filter = []
metric_name_filter = []


def generate_metric_dataset_outcome():
    load_test_metrics()
    for m in metric_fixtures:
        if metric_type_filter and not any(isinstance(m.metric, t) for t in metric_type_filter):
            continue
        if metric_name_filter and not any(m.name == n for n in metric_name_filter):
            continue
        yield from generate_dataset_outcome(m)


def pytest_generate_tests(metafunc: Metafunc):
    if metafunc.definition.name != "test_metric":
        return
    parameters = [
        ([m, d, o], f"{m.name}-{d.name or i}-{o.__class__.__name__}")
        for m, i, d, o in generate_metric_dataset_outcome()
    ]
    metafunc.parametrize(
        "tmetric,tdataset,outcome", [ParameterSet(values, values[0].marks, id_) for values, id_ in parameters]
    )
