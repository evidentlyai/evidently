from pprint import pprint

import pandas as pd

from evidently import ColumnMapping
from evidently.base_metric import ColumnName
from evidently.utils.data_preprocessing import create_data_definition


def old_evidently():
    from evidently.report import Report

    from evidently.metrics import ColumnDriftMetric
    from evidently.options import DataDriftOptions
    DataDriftOptions.__fields__["nbinsx"].default = 2
    report = Report(metrics=[
        ColumnDriftMetric("a")
    ])

    ref = pd.DataFrame([{"a": 0}, {"a": 1}, {"a": 2}])
    cur = pd.DataFrame([{"a": 0}, {"a": 0}, {"a": 0}])
    report.run(reference_data=ref, current_data=cur, column_mapping=ColumnMapping(numerical_features=["a"]))

    pprint(report.as_dict()["metrics"][0]["result"])
    result = {'column_name': 'a',
              'column_type': 'num',
              'current': {'small_distribution': {'x': [-0.5, 0.0, 0.5], 'y': [0.0, 2.0]}},
              'drift_detected': True,
              'drift_score': 0.04978706836786395,
              'reference': {'small_distribution': {'x': [0.0, 1.0, 2.0],
                                                   'y': [0.3333333333333333,
                                                         0.6666666666666666]}},
              'stattest_name': 'chi-square p_value',
              'stattest_threshold': 0.05}


def new():
    from evidently2.metrics.drift.column_drift_metric import ColumnDriftMetric
    from evidently.options import DataDriftOptions
    DataDriftOptions.__fields__["nbinsx"].default = 2

    metric = ColumnDriftMetric(column_name=ColumnName.from_any("a"))

    ref = pd.DataFrame([{"a": 0}, {"a": 1}, {"a": 2}])
    cur = pd.DataFrame([{"a": 0}, {"a": 0}, {"a": 0}])
    from evidently2.core.calculation import InputData
    data = InputData(current_data=cur, reference_data=ref,
                     data_definition=create_data_definition(ref, cur, ColumnMapping(numerical_features=["a"])))

    result = metric.calculate(data)
    # print(result)
    print(result.drift_score.get_result())  # 0.04978706836786395
    print(result.drift_detected.get_result())  # True
    print(result.current_small_distribution.get_result())  # ([0.0, 2.0], [-0.5, 0.0, 0.5])
    print(result.reference_small_distribution.get_result())  # ([0.3333333333333333, 0.6666666666666666], [0.0, 1.0, 2.0])


if __name__ == '__main__':
    old_evidently()
    new()
