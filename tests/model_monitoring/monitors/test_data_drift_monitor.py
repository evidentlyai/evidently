from evidently.model_monitoring.monitors.data_drift import DataDriftMonitor


def test_monitor_id():
    assert DataDriftMonitor().monitor_id() == "data_drift"
