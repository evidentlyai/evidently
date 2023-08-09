from pprint import pprint

import pandas as pd

from evidently import ColumnMapping
from evidently2.core.calculation import Context
from evidently2.core.calculation import InputValue
from evidently2.core.calculation import get_all_calculations
from evidently2.core.calculation import partial_calculations
from evidently.base_metric import ColumnName
from evidently.utils.data_preprocessing import create_data_definition


def old_evidently():
    from evidently.metrics import ColumnDriftMetric
    from evidently.options import DataDriftOptions
    from evidently.report import Report

    DataDriftOptions.__fields__["nbinsx"].default = 2
    report = Report(metrics=[ColumnDriftMetric("a")])

    ref = pd.DataFrame([{"a": 0}, {"a": 1}, {"a": 2}])
    cur = pd.DataFrame([{"a": 0}, {"a": 0}, {"a": 0}])
    report.run(reference_data=ref, current_data=cur, column_mapping=ColumnMapping(numerical_features=["a"]))

    pprint(report.as_dict()["metrics"][0]["result"])
    result = {
        "column_name": "a",
        "column_type": "num",
        "current": {"small_distribution": {"x": [-0.5, 0.0, 0.5], "y": [0.0, 2.0]}},
        "drift_detected": True,
        "drift_score": 0.04978706836786395,
        "reference": {"small_distribution": {"x": [0.0, 1.0, 2.0], "y": [0.3333333333333333, 0.6666666666666666]}},
        "stattest_name": "chi-square p_value",
        "stattest_threshold": 0.05,
    }


def new():
    from evidently2.metrics.drift.column_drift_metric import ColumnDriftMetric
    from evidently.options import DataDriftOptions

    DataDriftOptions.__fields__["nbinsx"].default = 2

    metric = ColumnDriftMetric(column_name=ColumnName.from_any("a"))

    ref = pd.DataFrame([{"a": 0}, {"a": 1}, {"a": 2}])
    cur = pd.DataFrame([{"a": 0}, {"a": 0}, {"a": 0}])
    from evidently2.core.calculation import InputData

    data = InputData(
        current_data=cur,
        reference_data=ref,
        data_definition=create_data_definition(ref, cur, ColumnMapping(numerical_features=["a"])),
    )

    with Context.new():
        result = metric.calculate(data)
    # pprint(result.get_result().dict())
    result_dict = {
        "column_name": "a",
        "column_type": "Numerical",
        "current_small_distribution": {
            "type": "evidently.metric_results.Distribution",
            "x": [-0.5, 0.0, 0.5],
            "y": [0.0, 2.0],
        },
        "drift_detected": True,
        "drift_score": 0.04978706836786395,
        "reference_small_distribution": {
            "type": "evidently.metric_results.Distribution",
            "x": [0.0, 1.0, 2.0],
            "y": [0.3333333333333333, 0.6666666666666666],
        },
        "stattest_name": "chi-square p_value",
        "stattest_threshold": 0.05,
        "type": "evidently2.metrics.drift.column_drift_metric.ColumnDriftResultCalculation",
    }
    column_mapping = ColumnMapping(numerical_features=["a"])
    from evidently2.core.suite import Report

    report = Report(metrics=[metric])
    profile = report.create_reference_profile(ref, column_mapping)

    report2 = profile.run(cur)

    pprint(report2.as_dict())

    # dd = create_data_definition(ref, cur, ColumnMapping(numerical_features=["a"]))
    # data = InputData(
    #     current_data=None,
    #     reference_data=ref,
    #     data_definition=dd,
    # )
    #
    # with Context.new() as ctx1:
    #     result = metric.calculate(data)
    #     skipping, deps = partial_calculations(result)
    #
    #     profile = ctx1.get_profile(list(deps))
    #
    # with Context.new() as ctx2:
    #     ctx2.add_profile(profile)
    #
    #     # data = InputData(current_data=cur, reference_data=None, data_definition=dd)
    #
    #     # result2 = metric.calculate(data)
    #     #
    #     # print(result2.get_result().dict())
    #     ctx2.results[InputValue(id="current")] = cur
    #     pprint(result.get_result().dict())
    # pprint(result.dict()["drift_score"])

    # for calc, deps in get_all_calculations(result).items():
    #     print(repr(calc), ":", " ".join(repr(c) for c in deps))

    #
    # print("skip", skipping)
    # print("not skip", not_skipping)
    # pprint(get_all_calculations(result.drift_score))


if __name__ == "__main__":
    # old_evidently()
    new()
