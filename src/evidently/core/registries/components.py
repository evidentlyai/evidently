# ruff: noqa: E501
# fmt: off
from evidently.pydantic_utils import register_type_alias
from evidently.ui.service.components import DataStorageComponent
from evidently.ui.service.components import MetadataStorageComponent
from evidently.ui.service.components.snapshot_links import SnapshotDatasetLinksComponent
from evidently.ui.service.components.storage import BlobStorageComponent
from evidently.ui.service.components.storage import DatasetFileStorageComponent
from evidently.ui.service.components.storage import DatasetMetadataComponent
from evidently.ui.service.components.storage import StorageComponent

register_type_alias(DataStorageComponent, "evidently.ui.service.components.local_storage.InmemoryDataComponent", "inmemory")
register_type_alias(DataStorageComponent, "evidently.ui.service.storage.sql.components.SQLDataComponent", "sql")
register_type_alias(MetadataStorageComponent, "evidently.ui.service.components.local_storage.JsonMetadataComponent", "json_file")
register_type_alias(MetadataStorageComponent, "evidently.ui.service.storage.sql.components.SQLMetadataComponent", "sql")
register_type_alias(StorageComponent, "evidently.ui.service.components.storage.LocalStorageComponent", "local")
register_type_alias(StorageComponent, "evidently.ui.service.storage.sql.components.SQLStorageComponent", "sql")
register_type_alias(BlobStorageComponent, "evidently.ui.service.components.local_storage.FSSpecBlobComponent", "fsspec")
register_type_alias(BlobStorageComponent, "evidently.ui.service.storage.sql.components.SQLBlobComponent", "sql")

register_type_alias(DatasetFileStorageComponent, "evidently.ui.service.components.local_storage.FSSpecDatasetFileStorageComponent", "fsspec")
register_type_alias(DatasetFileStorageComponent, "evidently.ui.service.storage.sql.components.SQLDatasetFileStorageComponent", "sql")
register_type_alias(DatasetMetadataComponent, "evidently.ui.service.components.local_storage.JsonDatasetMetadataComponent", "json_file")
register_type_alias(DatasetMetadataComponent, "evidently.ui.service.storage.sql.components.SQLDatasetMetadataComponent", "sql")

register_type_alias(SnapshotDatasetLinksComponent, "evidently.ui.service.components.local_storage.FileSnapshotDatasetLinksComponent", "file")
register_type_alias(SnapshotDatasetLinksComponent, "evidently.ui.service.storage.sql.components.SQLSnapshotDatasetLinksComponent", "sql")
