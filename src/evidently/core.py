from enum import Enum


class ColumnType(Enum):
    Numerical = "num"
    Categorical = "cat"
    Text = "text"
    Datetime = "datetime"
    Date = "data"
    Id = "id"
    Unknown = "unknown"
