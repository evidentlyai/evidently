from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from pyspark.sql import DataFrame

from evidently import ColumnMapping
from evidently.base_metric import ColumnName, ColumnNotFound, DatasetType
from evidently.core import ColumnType
from evidently.utils.data_preprocessing import DataDefinition, create_data_definition

SparkSeries = DataFrame
SparkDataFrame = DataFrame

def create_data_definition_spark(
    reference_data: Optional["SparkDataFrame"], current_data: "SparkDataFrame", mapping: ColumnMapping
) -> DataDefinition:

    # todo
    dd = create_data_definition(
        reference_data.toPandas() if reference_data is not None else None, current_data.toPandas(), mapping
    )
    return dd

