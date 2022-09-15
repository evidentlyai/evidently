from evidently.model_monitoring.monitors.cat_target_drift import CatTargetDriftMonitor


def test_monitor_id():
    assert CatTargetDriftMonitor().monitor_id() == "cat_target_drift"
