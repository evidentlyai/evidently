import re
from collections import defaultdict
from typing import Dict
from typing import Set

import pandas as pd
import pytest

from evidently.legacy.base_metric import Metric
from evidently.legacy.report import Report
from tests.conftest import slow
from tests.conftest import smart_assert_equal
from tests.multitest.conftest import Error
from tests.multitest.conftest import TestOutcome
from tests.multitest.conftest import find_all_subclasses
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import REFRESH_FINGERPRINT_VALUES
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import generate_dataset_outcome
from tests.multitest.metrics.conftest import load_test_metrics
from tests.multitest.metrics.conftest import metric_fixtures


def _check_dataframe(report: Report, metric: Metric):
    if not metric.__class__.result_type().__config__.pd_include:
        # skipping not supported
        return
    df = report.as_dataframe()
    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize(
    "raw_data", [pytest.param(True, marks=[slow], id="raw_data"), pytest.param(False, id="agg_data")]
)
def test_metric(tmetric: TestMetric, tdataset: TestDataset, outcome: TestOutcome, raw_data, tmp_path):
    msg = (
        "wrong fingerprint.\n"
        "If you certain that new value is correct, you can refresh fingerprint tests by setting "
        "REFRESH_FINGERPRINT_VALUES = True in conftest.py and running tests once. Dont forget to turn it off after."
        "WARNING! Changing fingerprints is not backward-compatible, all users will have to do migrations"
    )
    assert tmetric.metric.get_fingerprint() == tmetric.fingerprint, msg
    report = Report(metrics=[tmetric.metric], options={"render": {"raw_data": raw_data}})

    if isinstance(outcome, Error):
        with pytest.raises(outcome.exception_type, match=outcome.match):
            report.run(
                reference_data=tdataset.reference,
                current_data=tdataset.current,
                column_mapping=tdataset.column_mapping,
                additional_data=tdataset.additional_data,
            )
            report._inner_suite.raise_for_error()
            assert not report.show()
        return

    report.run(
        reference_data=tdataset.reference,
        current_data=tdataset.current,
        column_mapping=tdataset.column_mapping,
        additional_data=tdataset.additional_data,
    )
    report._inner_suite.raise_for_error()
    assert report.show()
    assert report.json()
    _check_dataframe(report, tmetric.metric)

    outcome.check(report)

    path = str(tmp_path / "report.json")
    report.save(path)
    report2 = Report.load(path)

    smart_assert_equal(report2.as_dict(), report.as_dict())  # has nans
    report2.show()
    report2.save_html(str(tmp_path / "report.html"))


IGNORE_METRICS = {"MetricV2Adapter", "MetricV2PresetAdapter"}


def test_all_metrics_tested():
    load_test_metrics()
    all_metric_classes = find_all_subclasses(Metric)
    missing = []
    no_datasets = []
    for metric_class in all_metric_classes:
        if metric_class.__name__ in IGNORE_METRICS:
            continue
        if not any(m.metric.__class__ is metric_class for m in metric_fixtures):
            missing.append(metric_class)
        else:
            tms = [tm for tm in metric_fixtures if tm.metric.__class__ is metric_class]
            tests = []
            for tm in tms:
                tests.extend(generate_dataset_outcome(tm))
            if len(tests) == 0:
                no_datasets.append(metric_class)

    suggestion_template = """
@metric
def {snake_case}():
    return TestMetric("name={snake_case}", metric={cls}())
    """
    suggestion = "\n".join(
        suggestion_template.format(cls=m.__name__, snake_case=re.sub(r"(?<!^)(?=[A-Z])", "_", m.__name__).lower())
        for m in missing
    )
    imports = "\n".join("from {module} import {cls}".format(cls=m.__name__, module=m.__module__) for m in missing)
    print(imports)
    print(suggestion)
    assert len(missing) == 0, f"Missing metric fixtures for {missing}."

    no_datasets_str = "\n".join(mc.__name__ for mc in no_datasets)
    assert len(no_datasets) == 0, f"No datasets configured for metrics {no_datasets_str}"


def test_all_fingerprints_differ():
    metric_to_fingerprints: Dict[Metric, Set[str]] = defaultdict(set)
    fingerprint_to_metrics: Dict[str, Set[Metric]] = defaultdict(set)

    for tmetric in metric_fixtures:
        f = tmetric.metric.get_fingerprint()
        metric_to_fingerprints[tmetric.metric].add(f)
        fingerprint_to_metrics[f].add(tmetric.metric)

    for metric, fingerprints in metric_to_fingerprints.items():
        assert len(fingerprints) == 1, f"Metric {metric} has different fingerprints: {fingerprints}"

    for fingerprint, metrics in fingerprint_to_metrics.items():
        assert len(metrics) == 1, f"Metrics {metrics} has the same fingerprint {fingerprint}"


def test_refresh_mode_off():
    assert not REFRESH_FINGERPRINT_VALUES, "you forgot to turn off refresh mode"
