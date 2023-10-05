from pyspark.sql import DataFrame
from pyspark.sql.types import LongType, FloatType, IntegerType, ShortType, ByteType, DoubleType, DecimalType
from evidently.base_metric import ColumnName


def is_numeric_dtype(df: DataFrame, column: ColumnName):
    dtype = df.schema.fields[df.schema.names.index(column.name)].dataType

    return isinstance(dtype, (LongType, FloatType, IntegerType, ShortType, ByteType, DoubleType, DecimalType))
