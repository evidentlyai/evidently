import json

import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.metrics import InListValueCount
from evidently.metrics import OutListValueCount


@pytest.mark.parametrize("metric_class", [InListValueCount, OutListValueCount])
@pytest.mark.parametrize("with_reference", [False, True])
@pytest.mark.parametrize(
    "data,values,matched",
    [
        pytest.param(["NY", "NY", "LA", None], ["NY", "NY"], 2, id="repeated-strings"),
        pytest.param([1, 1, 2, None], [1, 1], 2, id="repeated-integers"),
        pytest.param([True, True, False, None], [True, True], 2, id="repeated-booleans"),
        pytest.param(["NY", "NY", 1, None], ["NY", "NY", 1, 1], 3, id="repeated-mixed-labels"),
        pytest.param(["NY", "NY", "LA", None], ["NY"], 2, id="unique-list-control"),
        pytest.param(["NY", "NY", "LA", None], ["missing", "missing"], 0, id="absent-control"),
        pytest.param(["NY", "NY", "LA", None], [], 0, id="empty-list-control"),
        pytest.param(["NY", "NY", "LA", None], [None, None, "NY"], 2, id="null-list-control"),
    ],
)
def test_list_membership_counts_rows_once(metric_class, with_reference, data, values, matched):
    dataset = Dataset.from_pandas(
        pd.DataFrame({"value": pd.Series(data, dtype=object)}),
        data_definition=DataDefinition(categorical_columns=["value"]),
    )
    metric = metric_class(column="value", values=values)
    snapshot = Report([metric]).run(dataset, dataset if with_reference else None)
    result = snapshot.dict()["metrics"][0]["value"]
    expected = matched if metric_class is InListValueCount else 3 - matched
    assert result["count"] == expected
    assert result["share"] == pytest.approx(expected / 3)
    assert metric.values == values


@pytest.mark.parametrize(
    "dtype,data,native,foreign,numerical",
    [
        pytest.param("int64", [1, 1, 2], 1, True, True, id="integer"),
        pytest.param("Int64", [1, 1, 2, None], 1, True, True, id="nullable-integer"),
        pytest.param("float64", [1.0, 1.0, 2.0], 1.0, True, True, id="integral-float"),
        pytest.param("bool", [True, True, False], True, 1, False, id="boolean"),
        pytest.param("boolean", [True, True, False, None], True, 1, False, id="nullable-boolean"),
        pytest.param("category", [1, 1, 2], 1, True, False, id="numeric-category"),
        pytest.param("int64", [0, 0, 2], 0, False, True, id="false-zero"),
    ],
)
@pytest.mark.parametrize("with_reference", [False, True])
@pytest.mark.parametrize("lookup", ["native", "foreign", "mixed", "reversed", "repeated"])
def test_list_value_count_pandas_matching(dtype, data, native, foreign, numerical, with_reference, lookup):
    # A single boolean does not match a numeric index (or vice versa), but pandas
    # resolves a mixed boolean/numeric lookup to the matching source position.
    values = {
        "native": [native],
        "foreign": [foreign],
        "mixed": [foreign, native],
        "reversed": [native, foreign],
        "repeated": [foreign, native, native],
    }[lookup]
    values_before = repr(values)
    definition = DataDefinition(**{("numerical_columns" if numerical else "categorical_columns"): ["value"]})
    current_frame = pd.DataFrame({"value": pd.Series(data, dtype=dtype)})
    reference_frame = pd.DataFrame({"value": pd.Series([data[0], data[2]], dtype=dtype)})
    current_before = current_frame.copy(deep=True)
    reference_before = reference_frame.copy(deep=True)
    current = Dataset.from_pandas(current_frame, data_definition=definition)
    reference = Dataset.from_pandas(reference_frame, data_definition=definition) if with_reference else None
    metrics = [metric_class(column="value", values=values) for metric_class in (InListValueCount, OutListValueCount)]
    config_before = [metric.json() for metric in metrics]
    report = Report(metrics, include_tests=True)
    snapshot = report.run(current, reference)
    result = snapshot.dict()
    matched = 0 if lookup == "foreign" else 2
    for actual, expected in zip(result["metrics"], [matched, 3 - matched]):
        assert actual["value"]["count"] == expected
        assert actual["value"]["share"] == pytest.approx(expected / 3)
    if with_reference:
        reference_matched = 0 if lookup == "foreign" else 1
        for metric, expected in zip(metrics, [reference_matched, 2 - reference_matched]):
            actual = snapshot.context.get_reference_metric_result(metric.get_fingerprint()).to_simple_dict()
            assert actual["count"] == expected
            assert actual["share"] == pytest.approx(expected / 2)
        # With matches, current count/share differ from reference by more than 10%.
        # Losing both matches would incorrectly turn these in-list tests green.
        in_tests = [
            test for test in result["tests"] if test["metric_config"]["metric_id"] == metrics[0].get_fingerprint()
        ]
        assert len(in_tests) == 2
        if lookup != "foreign":
            assert all(test["status"] == "FAIL" for test in in_tests)
    assert repr(values) == values_before
    assert [metric.json() for metric in metrics] == config_before
    pd.testing.assert_frame_equal(current_frame, current_before)
    pd.testing.assert_frame_equal(reference_frame, reference_before)
    assert json.loads(snapshot.json())["metrics"] == result["metrics"]
    again = report.run(current, reference).dict()["metrics"]
    assert [metric["value"] for metric in again] == [metric["value"] for metric in result["metrics"]]


@pytest.mark.parametrize("dtype", ["bool", "boolean", "int64", "Int64"])
@pytest.mark.parametrize("with_reference", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_list_value_count_equal_index_control(dtype, with_reference, reverse):
    numerical = dtype in ("int64", "Int64")
    data = [1, 1, 0] if numerical else [True, True, False]
    values = [True, False] if numerical else [1, 0]
    if reverse:
        values.reverse()
    definition = DataDefinition(**{("numerical_columns" if numerical else "categorical_columns"): ["value"]})
    current = Dataset.from_pandas(pd.DataFrame({"value": pd.Series(data, dtype=dtype)}), data_definition=definition)
    reference = (
        Dataset.from_pandas(
            pd.DataFrame({"value": pd.Series([data[0], data[2]], dtype=dtype)}), data_definition=definition
        )
        if with_reference
        else None
    )
    metrics = [metric_class(column="value", values=values) for metric_class in (InListValueCount, OutListValueCount)]
    config_before = [metric.json() for metric in metrics]
    values_before = repr(values)
    snapshot = Report(metrics).run(current, reference)
    # Preserve pandas reindex's existing equal-index shortcut, including order.
    # Nullable index equality also checks dtype, so it does not take this shortcut.
    matches = not reverse and dtype in ("bool", "int64")
    matched = 3 if matches else 0
    for actual, expected in zip(snapshot.dict()["metrics"], [matched, 3 - matched]):
        assert actual["value"]["count"] == expected
        assert actual["value"]["share"] == pytest.approx(expected / 3)
    if with_reference:
        matched = 2 if matches else 0
        for metric, expected in zip(metrics, [matched, 2 - matched]):
            actual = snapshot.context.get_reference_metric_result(metric.get_fingerprint()).to_simple_dict()
            assert actual["count"] == expected
            assert actual["share"] == pytest.approx(expected / 2)
    assert [metric.json() for metric in metrics] == config_before
    assert repr(values) == values_before
