# ruff: noqa: E501
# fmt: off
from evidently.pydantic_utils import register_type_alias
from evidently.ui.service.components import DataStorageComponent
from evidently.ui.service.components import MetadataStorageComponent
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import StorageComponent

register_type_alias(DataStorageComponent, "evidently.ui.service.components.local_storage.InmemoryDataComponent", "inmemory")
register_type_alias(DataStorageComponent, "evidently.ui.service.storage.sql.components.SQLDataComponent", "sql")
register_type_alias(MetadataStorageComponent, "evidently.ui.service.components.local_storage.JsonMetadataComponent", "json_file")
register_type_alias(MetadataStorageComponent, "evidently.ui.service.storage.sql.components.SQLMetadataComponent", "sql")
register_type_alias(StorageComponent, "evidently.ui.service.components.storage.LocalStorageComponent", "local")
register_type_alias(StorageComponent, "evidently.ui.service.storage.sql.components.SQLStorageComponent", "sql")
register_type_alias(BlobStorageComponent, "evidently.ui.service.components.local_storage.FSSpecBlobComponent", "fsspec")
register_type_alias(BlobStorageComponent, "evidently.ui.service.storage.sql.components.SQLBlobComponent", "sql")
