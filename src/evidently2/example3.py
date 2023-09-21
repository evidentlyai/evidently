import pandas as pd

from evidently2.core.calculation import Context, InputColumnData, InputValue


def main():
    data = pd.DataFrame({"a": [1,2], "b": [3,4]})

    # from evidently2.core.engines import pandas
    from evidently2.core.engines import spark
    from pyspark.sql import SparkSession
    session = SparkSession.builder.getOrCreate()
    data = session.createDataFrame(data)
    inp = InputValue(id="current").bind(data)

    calc = InputColumnData(input_data=inp, column="a")

    with Context.new():
        print(calc.get_result())


if __name__ == '__main__':
    main()