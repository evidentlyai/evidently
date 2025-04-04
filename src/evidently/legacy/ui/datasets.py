from enum import Enum
from typing import Dict

from evidently.legacy.core import ColumnType
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.utils.data_preprocessing import FeatureDefinition


class DatasetSourceType(Enum):
    # This values correspond dataset_sources table in db.
    # Changing this class care about data consistency manually: add/remove from db
    file = 1
    tracing = 2
    snapshot_builder = 3
    dataset = 4
    datagen = 5


def inject_feature_types_in_column_mapping(
    column_mapping: ColumnMapping, features_metadata: Dict[str, FeatureDefinition]
) -> ColumnMapping:
    if not features_metadata:
        return column_mapping

    feature_numerical = [
        feature.display_name or ""
        for feature in features_metadata.values()
        if feature.feature_type == ColumnType.Numerical
    ]
    feature_categorical = [
        feature.display_name or ""
        for feature in features_metadata.values()
        if feature.feature_type == ColumnType.Categorical
    ]
    feature_test = [
        feature.display_name or "" for feature in features_metadata.values() if feature.feature_type == ColumnType.Text
    ]

    if column_mapping.categorical_features:
        column_mapping.categorical_features = []
    else:
        column_mapping.categorical_features = feature_categorical
    if column_mapping.numerical_features:
        column_mapping.numerical_features.extend(feature_numerical)
    else:
        column_mapping.numerical_features = feature_numerical
    if column_mapping.text_features:
        column_mapping.text_features.extend(feature_test)
    else:
        column_mapping.text_features = feature_test
    return column_mapping


def get_dataset_name(is_report: bool, snapshot_id: SnapshotID, run_from: str, ds_type: str, subtype: str) -> str:
    prefix = "report" if is_report else "testsuite"
    return f"{prefix}-{ds_type}-{subtype}-{run_from}-{snapshot_id}"


def get_dataset_name_output_current(is_report: bool, snapshot_id: SnapshotID, run_from: str) -> str:
    return get_dataset_name(is_report, snapshot_id, run_from, "output", "current")


def get_dataset_name_output_reference(is_report: bool, snapshot_id: SnapshotID, run_from: str) -> str:
    return get_dataset_name(is_report, snapshot_id, run_from, "output", "reference")
