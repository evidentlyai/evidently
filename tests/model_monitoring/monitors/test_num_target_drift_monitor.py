import pandas as pd
from pytest import approx

from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring.monitors.num_target_drift import \
    NumTargetDriftMonitor
from evidently.pipeline.column_mapping import ColumnMapping
from tests.model_monitoring.helpers import collect_metrics_results


def test_monitor_id():
    assert NumTargetDriftMonitor().monitor_id() == "num_target_drift"


def test_num_target_drift_monitor() -> None:
    reference_data = pd.DataFrame(
        {
            "target": [1, 2, 2, 4, 5, 6],
            "prediction": [1, 2, 3, 4, 5, 6],
        }
    )
    current_data = pd.DataFrame(
        {
            "target": [1, 0],
            "prediction": [1, 2],
        }
    )
    data_mapping = ColumnMapping()
    evidently_monitoring = ModelMonitoring(monitors=[NumTargetDriftMonitor()], options=None)
    evidently_monitoring.execute(reference_data=reference_data, current_data=current_data, column_mapping=data_mapping)
    result = collect_metrics_results(evidently_monitoring.metrics())
    assert "num_target_drift:count" in result
    assert result["num_target_drift:count"] == [
        {"labels": {"dataset": "reference"}, "value": 6},
        {"labels": {"dataset": "current"}, "value": 2},
    ]
    assert "num_target_drift:drift" in result
    assert result["num_target_drift:drift"] == [
        {"labels": {"kind": "prediction"}, "value": approx(0.4285, 1e-3)},
        {"labels": {"kind": "target"}, "value": approx(0.2142, 1e-3)},
    ]

    assert "num_target_drift:current_correlations" in result
    assert result["num_target_drift:current_correlations"] == [
        {"labels": {"feature": "prediction", "feature_type": "num", "kind": "prediction"}, "value": 1.0},
        {"labels": {"feature": "target", "feature_type": "num", "kind": "target"}, "value": 1.0},
    ]
    assert "num_target_drift:reference_correlations" in result
    assert result["num_target_drift:reference_correlations"] == [
        {"labels": {"feature": "prediction", "feature_type": "num", "kind": "prediction"}, "value": 1.0},
        {"labels": {"feature": "target", "feature_type": "num", "kind": "target"}, "value": 1.0},
    ]
