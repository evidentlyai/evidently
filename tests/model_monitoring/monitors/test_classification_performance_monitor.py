from evidently.model_monitoring.monitors.classification_performance import ClassificationPerformanceMonitor


def test_monitor_id():
    assert (
        ClassificationPerformanceMonitor().monitor_id() == "classification_performance"
    )
