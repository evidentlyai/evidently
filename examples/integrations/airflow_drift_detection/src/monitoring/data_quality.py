from typing import Dict
from typing import List
from typing import Text
from typing import Tuple

from sqlalchemy import create_engine
from src.utils.db_utils import add_or_update_by_ts
from src.utils.db_utils import open_sqa_session
from src.utils.models import DataQualityTable
from src.utils.type_conv import numpy_to_standard_types


def parse_data_quality_report(data_quality_report: Dict) -> Dict:
    """Parse data quality report and return metrics results.
    Extracting Evidently metrics:
        - DatasetSummaryMetric

    Args:
        data_quality_report (Dict): Data quality report.

    Returns:
        Dict: Dataset summary results.
    """

    assert len(data_quality_report["metrics"]) == 1
    ds_summary_metric: Dict = data_quality_report["metrics"][0]
    assert ds_summary_metric["metric"] == "DatasetSummaryMetric"
    summary_metrics: Dict = ds_summary_metric["result"]["current"]

    remove_fields: List[Text] = [
        "id_column",
        "target",
        "prediction",
        "date_column",
        "nans_by_columns",
        "number_uniques_by_columns",
    ]

    # Remove unused fields
    for field in remove_fields:
        del summary_metrics[field]

    summary_metrics["summary_metric_number_of_columns"] = summary_metrics[
        "number_of_columns"
    ]
    del summary_metrics["number_of_columns"]

    summary_metrics = numpy_to_standard_types(summary_metrics)

    return summary_metrics


def parse_data_drift_report(data_drift_report: Dict) -> Tuple[Dict, Dict]:
    """Parse data drift report and return metrics results.
    Extracting Evidently metrics:
        - DatasetDriftMetric
        - DataDriftTable (only for prediction column)

    Args:
        data_drift_report (Dict): Data drift report.

    Returns:
        Tuple[Dict, Dict]:
            tuple of data drift and data drift prediction metric results.
    """

    metrics: Dict = {
        metric["metric"]: metric["result"] for metric in data_drift_report["metrics"]
    }

    dataset_result: Dict = metrics["DatasetDriftMetric"]
    dataset_result["ds_drift_metric_number_of_columns"] = dataset_result[
        "number_of_columns"
    ]
    del dataset_result["number_of_columns"]

    dataset_result = numpy_to_standard_types(dataset_result)

    return dataset_result


def commit_data_metrics_to_db(
    data_quality_report: Dict, data_drift_report: Dict, timestamp: float, db_uri: Text
) -> None:
    """Commit data metrics to database.

    Args:
        data_quality_report (Dict): Data quality report
        data_drift_report (Dict): Data drift report
        timestamp (float): Metrics calculation timestamp
    """

    engine = create_engine(db_uri)
    session = open_sqa_session(engine)

    dataset_summary_metric_result: Dict = parse_data_quality_report(data_quality_report)
    drift_report_results: Dict = parse_data_drift_report(data_drift_report)

    data_quality = DataQualityTable(
        **dataset_summary_metric_result, **drift_report_results, timestamp=timestamp
    )

    add_or_update_by_ts(session=session, record=data_quality)

    session.commit()
    session.close()
