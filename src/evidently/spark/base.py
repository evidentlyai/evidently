from typing import Optional

from pyspark.sql import DataFrame

from evidently import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.data_preprocessing import create_data_definition

SparkSeries = DataFrame
SparkDataFrame = DataFrame


def create_data_definition_spark(
    reference_data: Optional[DataFrame], current_data: DataFrame, mapping: ColumnMapping
) -> DataDefinition:

    # todo
    dd = create_data_definition(
        reference_data.toPandas() if reference_data is not None else None, current_data.toPandas(), mapping
    )
    return dd
