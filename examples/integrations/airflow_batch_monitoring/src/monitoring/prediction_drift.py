from typing import Dict
from typing import Text
from typing import Tuple

from sqlalchemy import create_engine
from src.utils.db_utils import add_or_update_by_ts
from src.utils.db_utils import open_sqa_session
from src.utils.models import PredictionDriftTable
from src.utils.type_conv import numpy_to_standard_types

from evidently.report import Report


def parse_prediction_drift_report(prediction_drift_report: Report) -> Tuple[Dict, Dict]:
    """Parse data drift report and return metrics results.
    Extracting Evidently metrics:
        - DatasetDriftMetric
        - DataDriftTable (only for prediction column)

    Args:
        prediction_drift_report (Report): Data drift report.

    Returns:
        Tuple[Dict, Dict]:
            tuple of data drift and data drift prediction metric results.
    """

    prediction_drift_report_dict = prediction_drift_report.as_dict()

    metrics: Dict = {
        metric["metric"]: metric["result"]
        for metric in prediction_drift_report_dict["metrics"]
    }

    print("METRICS: ", metrics)

    prediction_result: Dict = metrics["ColumnDriftMetric"]

    # Rename some fields to meet DB table names
    prediction_result["threshold"] = prediction_result.pop("stattest_threshold")

    # Remove items that doesn't fit DB model
    # (for example 'current', 'reference')
    db_model = PredictionDriftTable()
    metrics_keys = list(prediction_result.keys())
    for key in metrics_keys:
        if key not in db_model.__table__.columns.keys():
            prediction_result.pop(key)

    prediction_result = numpy_to_standard_types(prediction_result)

    return prediction_result


def commit_prediction_drift_metrics_to_db(
    drift_report_metrics: Dict, timestamp: float, db_uri: Text
) -> None:
    """Commit data metrics to database.

    Args:
        drift_report_metrics (Dict): Data drift report
        timestamp (float): Metrics calculation timestamp
    """

    engine = create_engine(db_uri)
    session = open_sqa_session(engine)

    data_drift_prediction = PredictionDriftTable(
        **drift_report_metrics, timestamp=timestamp
    )
    add_or_update_by_ts(session, data_drift_prediction)

    session.commit()
    session.close()
