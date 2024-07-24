from evidently.ui.type_aliases import SnapshotID


def get_dataset_name(is_report: bool, snapshot_id: SnapshotID, run_from: str, ds_type: str, subtype: str) -> str:
    prefix = "report" if is_report else "testsuite"
    return f"{prefix}-{ds_type}-{subtype}-{run_from}-{snapshot_id}"


def get_dataset_name_output_current(is_report: bool, snapshot_id: SnapshotID, run_from: str) -> str:
    return get_dataset_name(is_report, snapshot_id, run_from, "output", "current")


def get_dataset_name_output_reference(is_report: bool, snapshot_id: SnapshotID, run_from: str) -> str:
    return get_dataset_name(is_report, snapshot_id, run_from, "output", "reference")
