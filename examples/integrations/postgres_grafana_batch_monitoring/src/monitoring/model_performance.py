import numpy as np
from sqlalchemy import create_engine
from typing import Dict, List, Text

from config.db_config import DATABASE_URI
from src.utils.db_utils import open_sqa_session, add_or_update_by_ts
from src.utils.models import ModelPerformanceTable, TargetDriftTable
from src.utils.type_conv import numpy_to_standard_types


def parse_model_performance_report(model_performance_report: Dict) -> Dict:
    """Parse model performance report and return metrics results.
    Extracting Evidently metrics:
        - RegressionQualityMetric

    Args:
        model_performance_report (Dict): Model performance report.

    Returns:
        Dict: Regression quality result.
    """

    assert len(model_performance_report["metrics"]) == 1
    quality_metric: Dict = model_performance_report["metrics"][0]
    assert quality_metric["metric"] == "RegressionQualityMetric"
    raw_quality_metric_result: Dict = quality_metric["result"]
    quality_metric_result: Dict = {
        k: v
        for k, v in raw_quality_metric_result.items()
        if isinstance(v, (int, float, str, np.generic))
    }
    quality_metric_result = numpy_to_standard_types(quality_metric_result)

    return quality_metric_result


def parse_target_drift_report(target_drift_report: Dict) -> Dict:
    """Parse target drift report and return metrics results.
    Extracting Evidently metrics:
        - ColumnDriftMetric from target column

    Args:
        target_drift_report (Dict): Target drift report.

    Returns:
        Dict: Target drift result.
    """

    assert len(target_drift_report["metrics"]) == 1
    drift_metric: Dict = target_drift_report["metrics"][0]
    assert drift_metric["metric"] == "ColumnDriftMetric"
    raw_drift_metric_result: Dict = drift_metric["result"]
    drift_metric_result: Dict = {
        k: v
        for k, v in raw_drift_metric_result.items()
        if isinstance(v, (int, float, str, np.generic))
    }
    drift_metric_result = numpy_to_standard_types(drift_metric_result)
    remove_fields: List[Text] = ["column_name", "column_type"]

    for field in remove_fields:
        del drift_metric_result[field]

    return drift_metric_result


def commit_model_metrics_to_db(
    model_performance_report: Dict, target_drift_report: Dict, timestamp: float
) -> None:
    """Commit model metrics to database.

    Args:
        model_performance_report (Dict): Model performance report.
        target_drift_report (Dict): Target drift report.
        timestamp (float): Metrics calculation timestamp
    """

    engine = create_engine(DATABASE_URI)
    session = open_sqa_session(engine)

    model_quality_metric_result: Dict = parse_model_performance_report(
        model_performance_report
    )
    target_drift_metric_result: Dict = parse_target_drift_report(target_drift_report)

    model_performance = ModelPerformanceTable(
        **model_quality_metric_result, timestamp=timestamp
    )
    add_or_update_by_ts(session, model_performance)

    target_drift = TargetDriftTable(**target_drift_metric_result, timestamp=timestamp)
    add_or_update_by_ts(session, target_drift)

    session.commit()
    session.close()
