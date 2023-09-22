from pprint import pprint

import pandas as pd

from evidently2.core.calculation import Context
from evidently2.core.calculation import InputColumnData
from evidently2.core.calculation import InputValue
from evidently2.core.suite import Report
from evidently.metrics import ColumnMissingValuesMetric


def engines():
    data = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    # from evidently2.core.engines import pandas
    from pyspark.sql import SparkSession

    from evidently2.engines import spark

    session = SparkSession.builder.getOrCreate()
    data = session.createDataFrame(data)
    inp = InputValue(id="current").bind(data)

    calc = InputColumnData(input_data=inp, column="a")

    with Context.new():
        print(calc.get_result())


def old_compat():
    metric = ColumnMissingValuesMetric(column_name="a", missing_values=[0])

    report = Report(metrics=[metric])
    data = pd.DataFrame({"a": [1, 1, 0]})

    report.run(data, None)

    pprint(report.as_dict())


if __name__ == "__main__":
    # engines()
    old_compat()
