import numpy as np
import pandas as pd
import pytest
from pydantic import BaseModel
from pytest_spark.config import SparkConfigBuilder
from pytest_spark.util import reduce_logging

from evidently.utils.spark_compat import IS_PYSPARK_AVAILABLE

PANDAS_OR_SPARK_PARAMS = ["pandas", "spark"] if IS_PYSPARK_AVAILABLE else ["pandas"]

SPARK_ONLY = True

if SPARK_ONLY:
    PANDAS_OR_SPARK_PARAMS.remove("pandas")


def pytest_collection_modifyitems(config, items):
    if not IS_PYSPARK_AVAILABLE:
        skip_spark = pytest.mark.skip(reason="need pyspark to run spark related unit tests")
        for item in items:
            # TODO: validate that it covers both spark_session and pandas_or_spark_session (indirectly)
            if "spark_session" in item.fixturenames:
                item.add_marker(skip_spark)


# with regard to https://docs.pytest.org/en/stable/deprecations.html#calling-fixtures-directly
# it is necessary to copy some code from pytest_spark library


@pytest.fixture(scope="session", params=PANDAS_OR_SPARK_PARAMS)
def _pandas_or_spark_session(request):
    """Internal fixture for SparkSession instance.

    Yields SparkSession instance if it is supported by the pyspark
    version, otherwise yields None.

    Required to correctly initialize `spark_context` fixture after
    `spark_session` fixture.

    ..note::
        It is not possible to create SparkSession from the existing
        SparkContext.
    """
    if request.param == "pandas":
        yield None
        return

    try:
        from pyspark.sql import SparkSession
    except ImportError:
        raise Exception("pyspark is not configured and we should not be here")
    else:
        session = SparkSession.builder.config(conf=SparkConfigBuilder().get()).getOrCreate()

        yield session
        session.stop()


@pytest.fixture(scope="session")
def pandas_or_spark_session(_pandas_or_spark_session):
    """Return a Hive enabled SparkSession instance with reduced logging
    (session scope).

    Available from Spark 2.0 onwards.
    """

    if _pandas_or_spark_session is None:
        yield None

    else:
        reduce_logging(_pandas_or_spark_session.sparkContext)
        yield _pandas_or_spark_session


def smart_assert_equal(actual, expected):
    if isinstance(actual, BaseModel) and isinstance(expected, BaseModel) and actual.__class__ is expected.__class__:
        for field in actual.__fields__.values():
            smart_assert_equal(getattr(actual, field.name), getattr(expected, field.name))
        return
    if isinstance(actual, pd.Series):
        pd.testing.assert_series_equal(actual, expected)
        return
    if isinstance(actual, pd.DataFrame):
        pd.testing.assert_frame_equal(actual, expected)
        return
    np.testing.assert_equal(actual, expected)
