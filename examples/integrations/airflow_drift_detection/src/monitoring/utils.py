from evidently.report import Report


def detect_target_drift(target_drift_report: Report) -> bool:
    """
    Returns True if Target Drift is detected, else returns False.
    """

    report = target_drift_report.as_dict()
    return report["metrics"][0]["result"]["drift_detected"]


def detect_data_drift(data_drift_report: Report) -> bool:
    """
    Returns True if Data Drift is detected, else returns False.
    """

    report = data_drift_report.as_dict()
    return report["metrics"][0]["result"]["dataset_drift"]


def detect_prediction_drift(data_drift_report: Report) -> bool:
    """
    Returns True if Data Drift is detected, else returns False.
    """

    report = data_drift_report.as_dict()
    return report["metrics"][0]["result"]["dataset_drift"]
