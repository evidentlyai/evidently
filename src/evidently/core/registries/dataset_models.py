# ruff: noqa: E501
# fmt: off
from evidently.pydantic_utils import register_type_alias
from evidently.ui.service.datasets.data_source import DataSource
from evidently.ui.service.datasets.data_source import DataSourceDTO
from evidently.ui.service.datasets.filters import FilterByNumber
from evidently.ui.service.datasets.filters import FilterByString

register_type_alias(DataSource, "evidently.ui.service.datasets.data_source.DatasetDataSource", "evidently:data_source:DatasetDataSource")
register_type_alias(DataSource, "evidently.ui.service.datasets.data_source.FileDataSource", "evidently:data_source:FileDataSource")
register_type_alias(DataSource, "evidently.ui.service.datasets.data_source.SortedFilteredDataSource", "evidently:data_source:SortedFilteredDataSource")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.EqualFilter", "eq")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.GTEFilter", "gte")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.GTFilter", "gt")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.LTEFilter", "lte")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.LTFilter", "lt")
register_type_alias(FilterByNumber, "evidently.ui.service.datasets.filters.NotEqualFilter", "not_eq")
register_type_alias(FilterByString, "evidently.ui.service.datasets.filters.ContainsStrFilter", "contains")
register_type_alias(FilterByString, "evidently.ui.service.datasets.filters.EndsWithFilter", "ends_with")
register_type_alias(FilterByString, "evidently.ui.service.datasets.filters.StartsWithFilter", "starts_with")
register_type_alias(DataSourceDTO, "evidently.ui.service.datasets.data_source.DatasetDataSourceDTO", "evidently:data_source_dto:DatasetDataSourceDTO")
register_type_alias(DataSourceDTO, "evidently.ui.service.datasets.data_source.FileDataSourceDTO", "evidently:data_source_dto:FileDataSourceDTO")
