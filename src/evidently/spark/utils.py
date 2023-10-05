from typing import Any
from typing import Callable
from typing import Tuple
from typing import Union

from pyspark.sql import Column
from pyspark.sql import DataFrame
from pyspark.sql.types import ByteType
from pyspark.sql.types import DecimalType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import ShortType

from evidently.base_metric import ColumnName


def is_numeric_dtype(df: DataFrame, column: ColumnName):
    dtype = df.schema.fields[df.schema.names.index(column.name)].dataType

    return isinstance(dtype, (LongType, FloatType, IntegerType, ShortType, ByteType, DoubleType, DecimalType))


def calculate_stats(df: DataFrame, column_name: str, *funcs: Callable[[str], Column]) -> Union[Tuple, Any]:
    cols = [f(column_name).alias(str(i)) for i, f in enumerate(funcs)]
    result = df.select(cols).first()
    if result is None:
        raise ValueError("Empty DataFrame")
    if len(funcs) == 1:
        return result["0"]
    return tuple(result[str(i)] for i in range(len(funcs)))
