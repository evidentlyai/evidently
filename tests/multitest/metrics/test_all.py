import re

import numpy
import pytest

from evidently.base_metric import Metric
from evidently.report import Report
from tests.multitest.conftest import Error
from tests.multitest.conftest import TestOutcome
from tests.multitest.conftest import find_all_subclasses
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import generate_dataset_outcome
from tests.multitest.metrics.conftest import load_test_metrics
from tests.multitest.metrics.conftest import metric_fixtures


@pytest.mark.parametrize("raw_data", [True, False], ids=["raw_data", "agg_data"])
def test_metric(tmetric: TestMetric, tdataset: TestDataset, outcome: TestOutcome, raw_data, tmp_path):
    report = Report(metrics=[tmetric.metric], options={"render": {"raw_data": raw_data}})

    if isinstance(outcome, Error):
        with pytest.raises(outcome.exception_type):
            report.run(
                reference_data=tdataset.reference, current_data=tdataset.current, column_mapping=tdataset.column_mapping
            )
            report._inner_suite.raise_for_error()
            assert not report.show()
        return

    report.run(reference_data=tdataset.reference, current_data=tdataset.current, column_mapping=tdataset.column_mapping)
    report._inner_suite.raise_for_error()
    assert report.show()
    assert report.json()

    if tmetric.additional_check is not None:
        tmetric.additional_check(report)

    path = str(tmp_path / "report.json")
    report._save(path)
    report2 = Report._load(path)

    numpy.testing.assert_equal(report2.as_dict(), report.as_dict())  # has nans
    report2.show()
    report2.save_html(str(tmp_path / "report.html"))


def test_all_metrics_tested():
    load_test_metrics()
    all_metric_classes = find_all_subclasses(Metric)
    missing = []
    no_datasets = []
    for metric_class in all_metric_classes:
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
    return TestMetric("{snake_case}", {cls}())
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
