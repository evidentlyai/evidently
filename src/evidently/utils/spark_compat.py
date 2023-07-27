import pandas as pd

IS_PYSPARK_AVAILABLE = True
try:
    import pyspark  # noqa: F401
except ImportError:
    IS_PYSPARK_AVAILABLE = False

if IS_PYSPARK_AVAILABLE:
    from ._spark_compat import Series
    from ._spark_compat import concat
    from ._spark_compat import histogram
    from ._spark_compat import spark_warn
else:
    from numpy import histogram

    Series = pd.Series
    concat = pd.concat

    def spark_warn(*args, **kwargs):
        pass


__all__ = ["IS_PYSPARK_AVAILABLE", "histogram", "spark_warn", "Series", "concat"]
