from enum import Enum
from typing import List

from evidently._pydantic_compat import BaseModel
from evidently.core.datasets import DataDefinition


class ColumnDataType(Enum):
    Numerical = "numerical"
    String = "string"
    Datetime = "datetime"


class DatasetColumn(BaseModel):
    name: str
    type: ColumnDataType
    is_index: bool = False


class Metadata(BaseModel):
    name: str
    description: str
    row_count: int
    data_definition: DataDefinition
    columns: List[DatasetColumn]


class DatasetPagination(BaseModel):
    items: List[List]
    metadata: Metadata
    page_size: int
    current_page: int
    total_pages: int
