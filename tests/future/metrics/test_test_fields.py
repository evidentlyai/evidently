import subprocess
from inspect import isabstract
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

import pytest
from typing_inspect import get_origin

from evidently import Dataset
from evidently import Report
from evidently._pydantic_compat import ModelField
from evidently.core.metric_types import ColumnMetric
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricTest
from evidently.core.metric_types import MetricTestResult
from evidently.core.metric_types import TestStatus
from evidently.metrics import FBetaTopK
from evidently.metrics import PrecisionTopK
from evidently.metrics import RecallTopK
from evidently.metrics.column_statistics import CategoryCount
from evidently.metrics.column_statistics import InListValueCount
from evidently.metrics.column_statistics import InRangeValueCount
from evidently.metrics.column_statistics import OutListValueCount
from evidently.metrics.column_statistics import OutRangeValueCount
from evidently.metrics.column_statistics import ValueDriftTest
from evidently.metrics.recsys import MAP
from evidently.metrics.recsys import MRR
from evidently.metrics.recsys import NDCG
from evidently.metrics.recsys import Diversity
from evidently.metrics.recsys import HitRate
from evidently.metrics.recsys import Personalization
from evidently.metrics.recsys import ScoreDistribution
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import gte
from evidently.tests import is_in
from evidently.tests import lt
from evidently.tests import lte
from evidently.tests import not_eq
from evidently.tests import not_in
from evidently.tests.categorical_tests import IsInMetricTest
from evidently.tests.categorical_tests import NotInMetricTest
from evidently.tests.numerical_tests import EqualMetricTest
from evidently.tests.numerical_tests import GreaterOrEqualMetricTest
from evidently.tests.numerical_tests import GreaterThanMetricTest
from evidently.tests.numerical_tests import LessOrEqualMetricTest
from evidently.tests.numerical_tests import LessThanMetricTest
from evidently.tests.numerical_tests import NotEqualMetricTest
from tests.conftest import load_all_subtypes

from ..tests.test_generic_tests_creation import StubMetric
from .all_metrics_tests import all_metrics_test

COPY_TO_CLIPBOARD = True

load_all_subtypes(Metric)
load_all_subtypes(MetricTest)


def iter_type_test_fields(metric_type: Type[Metric]) -> Iterable[Tuple[str, ModelField]]:
    for field_name, field in metric_type.__fields__.items():
        if not _is_test_field(field):
            continue
        yield field_name, field


def _get_tested_test_fields(metric: Metric) -> List[str]:
    res = []
    for field_name, _ in iter_type_test_fields(metric.__class__):
        if getattr(metric, field_name):
            res.append(field_name)
    return res


def _iter_test_types(obj) -> Iterable[Type[MetricTest]]:
    if isinstance(obj, MetricTest):
        yield obj.__class__
        return
    if isinstance(obj, dict):
        yield from (mt for v in obj.values() for mt in _iter_test_types(v))
        return
    if isinstance(obj, list):
        yield from (mt for v in obj for mt in _iter_test_types(v))
        return
    raise NotImplementedError(obj.__class__)


def _get_tested_test_types(metric: Metric, test_field: str) -> Set[Type[MetricTest]]:
    tests = getattr(metric, test_field)
    if not tests:
        return set()
    return set(_iter_test_types(tests))


def _get_all_test_fields(metric_type: Type[Metric]) -> List[str]:
    return [fn for fn, _ in iter_type_test_fields(metric_type)]


tested_statuses = [TestStatus.SUCCESS, TestStatus.FAIL]

METRIC_TEST_TYPE_MAPPING: Dict[Type[MetricTest], Tuple[Callable, str]] = {
    EqualMetricTest: (eq, "0"),
    NotEqualMetricTest: (not_eq, "0"),
    NotInMetricTest: (not_in, "[0]"),
    IsInMetricTest: (is_in, "[0]"),
    GreaterThanMetricTest: (gt, "0"),
    LessThanMetricTest: (lt, "0"),
    LessOrEqualMetricTest: (lte, "0"),
    GreaterOrEqualMetricTest: (gte, "0"),
}

METRIC_TEST_TYPE_MAPPING_INDEX = {tt: f.__name__ for tt, (f, _) in METRIC_TEST_TYPE_MAPPING.items()}

TEST_FIELD_FACTORY_MAPPING: Dict[Type, Callable[[str], str]] = {dict: lambda x: f"{{0: [{x}]}}"}

METRIC_ARGS: Dict[Type[Metric], str] = {
    CategoryCount: "category=True, ",
    FBetaTopK: "k=1, ",
    HitRate: "k=1, ",
    MAP: "k=1, ",
    RecallTopK: "k=1, ",
    PrecisionTopK: "k=1, ",
    MRR: "k=1, ",
    NDCG: "k=1, ",
    ScoreDistribution: "k=1, ",
    InListValueCount: "values=[1], ",
    OutListValueCount: "values=[1], ",
    InRangeValueCount: "left=0, right=2, ",
    OutRangeValueCount: "left=0, right=2, ",
    Diversity: "k=1, item_features=[], ",
    # Serendipity: "k=1, item_features=[], ",
    # Novelty: "k=1, ",
    Personalization: "k=1, ",
    # PopularityBiasMetric: "k=1, ",
}

SKIP_TEST_TYPES = {ValueDriftTest}
SKIP_METRIC_TYPES = {StubMetric}


def test_all_metric_tested():
    """If this test fails, you either added new metric or new test condition
    In all_metrics_tests.py there is a list of all combinations which is now incomplete.
    You can add output of the assert in this test to the list. Might need to tweak a little.

    New Metric:
    You can add additional kwargs in METRIC_ARGS constant for this test to generate valid test cases.
    New Test Condition:
    Add corresponding alias to METRIC_TEST_TYPE_MAPPING

    After you added new test cases, run test_all_test_fields.
    You need to adjust test conditions for tests to pass. You can do it manually or semi-automatically if TRY_FIX=True.
    Just run test_all_test_fields and it will rewrite test conditions directly in all_metrics_tests.py.
    It re-writes only failing tests so you can adjust conditions manually.
    If you added new test condition you need to add logic for it in fix(line) function.
    """
    all_metric_types = set(s for s in Metric.__subtypes__() if not isabstract(s)) - SKIP_METRIC_TYPES
    all_metric_types = {mt for mt in all_metric_types if hasattr(mt, "__calculation_type__")}
    all_test_types = set(t for t in MetricTest.__subtypes__() if not isabstract(t)) - SKIP_TEST_TYPES

    metrics_tests_set = {
        (metric.__class__, test_field, test_type, status)
        for (_, metric, status, _) in all_metrics_test
        for test_field in _get_tested_test_fields(metric)
        for test_type in _get_tested_test_types(metric, test_field)
    }
    all_metric_tests = {
        (metric_type, test_field, test_type, status)
        for metric_type in all_metric_types
        for test_field in _get_all_test_fields(metric_type)
        for test_type in all_test_types
        for status in tested_statuses
    }

    missing_tests = list(all_metric_tests - metrics_tests_set)
    missing_tests = sorted(missing_tests, key=lambda t: (t[0].__name__, t[1], t[2].__name__, t[3].name))

    def _fmt(tp) -> str:
        metric_type, test_field, test_type, status = tp
        test_callable = METRIC_TEST_TYPE_MAPPING.get(test_type, None)
        test_callable_name = (
            f"{test_callable[0].__name__}({test_callable[1]})" if test_callable else f"{test_type.__name__}(...)"
        )

        test_field_type = get_origin(metric_type.__fields__[test_field].outer_type_)
        test_field_value_str = (
            TEST_FIELD_FACTORY_MAPPING[test_field_type](test_callable_name)
            if test_field_type in TEST_FIELD_FACTORY_MAPPING
            else f"[{test_callable_name}]"
        )
        metric_args = METRIC_ARGS.get(metric_type, "")
        if issubclass(metric_type, ColumnMetric):
            metric_args = f'column="a", {metric_args}'
        dataset_name = "simple_dataset"
        if "recsys" in metric_type.__module__:
            dataset_name = "recsys_dataset"
        return f"({dataset_name}, {metric_type.__name__}({metric_args}{test_field}={test_field_value_str}), TestStatus.{status.name})"

    format_missing = ", ".join(map(_fmt, missing_tests))
    if len(missing_tests) > 0 and COPY_TO_CLIPBOARD:
        try:
            subprocess.run(
                "pbcopy", text=True, input="\n".join(line + "," for line in map(_fmt, missing_tests)), check=False
            )
        except subprocess.CalledProcessError:
            pass
    assert len(missing_tests) == 0, "Missing tests for metric fields: {}".format(format_missing)


def _is_test_field(field: ModelField) -> bool:
    if field.outer_type_ is bool:
        return False
    return "tests" in field.name


def _make_id(tp):
    _, metric, results, _ = tp
    if isinstance(results, TestStatus):
        results = [results]
    tested_fields = _get_tested_test_fields(metric)
    tested_fields_str = ", ".join(tested_fields)
    tested_types = ", ".join(
        METRIC_TEST_TYPE_MAPPING_INDEX[t] for tf in tested_fields for t in _get_tested_test_types(metric, tf)
    )
    return f"test_field-{metric.__class__.__name__}-{tested_fields_str}-{tested_types}-{', '.join(r.value for r in results)})"


TRY_FIX = True


def _try_fix(metric: Metric, expected_results: List[TestStatus], test_result: MetricTestResult):
    path = Path(__file__).parent / "all_metrics_tests.py"
    lines = path.read_text().splitlines()
    tested_fields = _get_tested_test_fields(metric)
    tested_tests = [tt for tf in tested_fields for tt in _get_tested_test_types(metric, tf)]

    def line_check(x):
        return (
            " " + metric.__class__.__name__ + "(" in x
            and all(ts.value in x for ts in expected_results)
            and all(f"({tf}=" in x or f" {tf}=" in x for tf in tested_fields)
            and all("[" + METRIC_TEST_TYPE_MAPPING_INDEX[tt] + "(" in x for tt in tested_tests)
        )

    matched_lines = [line for line in lines if line_check(line)]
    if not len(matched_lines) == 1:
        return
    matched_line = matched_lines[0]

    def fix(ln: str) -> str:
        if "[gt" in ln:
            value = "555" if "FAIL" in ln else "-555"
            return ln.replace("(0)", f"({value})").replace("(-1)", f"({value})")
        if "[lt" in ln:
            value = "-555" if "FAIL" in ln else "555"
            return ln.replace("(0)", f"({value})").replace("(-1)", f"({value})")
        if "[eq" in ln:
            try:
                value = test_result.description.split("Actual value ")[1].split(" ")[0]
            except IndexError:
                return ln
            value = value if "SUCCESS" in ln else "555"
            if "." in value and len(value) > 4:
                value = f"ApproxValue({value}, absolute=0.01)"
            return ln.replace("(0)", f"({value})")
        if "[not_eq" in ln:
            try:
                value = test_result.description.split("Actual value ")[1].split(" ")[0]
            except IndexError:
                return ln
            value = "555" if "SUCCESS" in ln else value
            if "." in value and len(value) > 4:
                value = f"ApproxValue({value}, absolute=0.01)"
            return ln.replace("(0)", f"({value})")
        if "[is_in" in ln:
            try:
                value = test_result.description.split("Actual value: ")[1].split(" ")[0]
            except IndexError:
                return ln
            value = value if "SUCCESS" in ln else "555"
            if "." in value and len(value) > 4:
                value = f"ApproxValue({value}, absolute=0.01)"
            return ln.replace("[0]", f"[{value}]")
        if "[not_in" in ln:
            try:
                value = test_result.description.split("Actual value: ")[1].split(" ")[0]
            except IndexError:
                return ln
            value = "555" if "SUCCESS" in ln else value
            if "." in value and len(value) > 4:
                value = f"ApproxValue({value}, absolute=0.01)"
            return ln.replace("[0]", f"[{value}]")

        return ln

    fixed_line = fix(matched_line)
    path.write_text("\n".join(line if line != matched_line else fixed_line for line in lines))


FILTER_METRICS = []

if FILTER_METRICS:
    all_metrics_test = [t for t in all_metrics_test if t[1].__class__ in FILTER_METRICS]


@pytest.mark.parametrize(
    "dataset,metric,expected_results,additional_data", all_metrics_test, ids=list(map(_make_id, all_metrics_test))
)
def test_all_test_fields(
    dataset: Dataset, metric: Metric, expected_results: Union[TestStatus, List[TestStatus]], additional_data
):
    report = Report([metric])
    run = report.run(dataset, dataset, additional_data=additional_data)
    test_results = run._context._metrics[metric.get_fingerprint()].tests
    statuses = [t.status for t in test_results]
    if isinstance(expected_results, TestStatus):
        expected_results = [expected_results]
    if statuses != expected_results and TRY_FIX:
        _try_fix(metric, expected_results, test_results[0])
    assert statuses == expected_results, "\n".join(
        f"{tr.description} should {status.value}" for tr, status in zip(test_results, expected_results)
    )
