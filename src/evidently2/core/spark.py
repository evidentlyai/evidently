from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

try:
    import pyspark

    SPARK_AVAILABLE = True
except ImportError:
    SPARK_AVAILABLE = False


from evidently import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.data_preprocessing import create_data_definition

if TYPE_CHECKING:
    from pyspark.sql import Column as SparkColumn
    from pyspark.sql import DataFrame as SparkDataFrame
else:
    SparkDataFrame = SparkColumn = Any


def create_data_definition_spark(
    reference_data: Optional["SparkDataFrame"], current_data: "SparkDataFrame", mapping: ColumnMapping
) -> DataDefinition:

    # todo
    dd = create_data_definition(
        reference_data.toPandas() if reference_data is not None else None, current_data.toPandas(), mapping
    )
    return dd


def is_spark_data(data):
    if not SPARK_AVAILABLE:
        return False
    from pyspark.sql import DataFrame

    return isinstance(data, DataFrame)


def single_column(data: "SparkDataFrame") -> "SparkColumn":
    cols = data.columns
    if len(cols) != 1:
        raise ValueError(f"DataFrame should only have one column, had {cols}")
    return data[cols[0]]
