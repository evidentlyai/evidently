def convert_pandas_to_spark_df_if_necessary(dataset, maybe_spark_session):
    if maybe_spark_session is None:
        return dataset

    if dataset is None:
        return None

    # let's try Pandas API on Spark default functionality
    import pyspark.pandas as ps

    pandas_spark_current_df = ps.from_pandas(dataset)

    # pytest tests/metrics/data_quality/test_column_quantile_metric.py -v
    # gives 3 more PASSED vs default pd.from_pandas implementation
    # fixup_pandas_df_for_big_data(dataset)
    # spark_current_df = maybe_spark_session.createDataFrame(dataset)
    # pandas_spark_current_df = spark_current_df.pandas_api()

    return pandas_spark_current_df


def fixup_json_if_necessary(json: dict, spark_fixup_json: dict, maybe_spark_session):
    if maybe_spark_session is None:
        return json

    json.update(spark_fixup_json)
    return json
