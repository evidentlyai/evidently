from evidently.model_monitoring.monitors.num_target_drift import NumTargetDriftMonitor


def test_monitor_id():
    assert NumTargetDriftMonitor().monitor_id() == "num_target_drift"
