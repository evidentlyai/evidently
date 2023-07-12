import argparse
import logging
from pathlib import Path
from typing import List
from typing import Text

import pandas as pd
import pendulum
from config import COLUMN_MAPPING
from config import MONITORING_DB_URI
from config import PREDICTIONS_DIR
from config import REFERENCE_DIR
from config import TARGET_DRIFT_REPORTS_DIR
from src.monitoring.model_performance import commit_model_metrics_to_db
from src.monitoring.utils import detect_target_drift
from src.pipelines.monitor_data import prepare_current_data
from src.utils.utils import get_batch_interval

from evidently.metrics import ColumnDriftMetric
from evidently.metrics import RegressionQualityMetric
from evidently.report import Report

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("MONITOR_MODEL")


def monitor_model(ts: pendulum.DateTime, interval: int = 60) -> None:
    """Build and save monitoring reports.

    Args:
        ts (pendulum.DateTime, optional): Timestamp.
        interval (int, optional): Interval. Defaults to 60.
    """

    LOGGER.info("Start the pipeline")

    # Prepare current data
    start_time, end_time = get_batch_interval(ts, interval)
    current_data = prepare_current_data(start_time, end_time)

    # Get predictions for the current data
    filename = pendulum.parse(end_time).to_date_string()
    path = Path(f"{PREDICTIONS_DIR}/{filename}.parquet")
    predictions = pd.read_parquet(path)

    # Merge current data with predictions
    current_data = current_data.merge(predictions, on="uuid", how="left")
    current_data = current_data.fillna(current_data.median(numeric_only=True)).fillna(
        -1
    )

    if current_data.shape[0] == 0:

        # Skip monitoring if current data is empty
        # Usually it may happen for few first batches
        LOGGER.info("Current data is empty!")
        LOGGER.info("Skip model monitoring")

    else:

        # Prepare reference data
        ref_path = Path(f"{REFERENCE_DIR}/reference_data_2021-01.parquet")
        ref_data = pd.read_parquet(ref_path)
        columns: List[Text] = (
            COLUMN_MAPPING.numerical_features
            + COLUMN_MAPPING.categorical_features
            + [COLUMN_MAPPING.target, COLUMN_MAPPING.prediction]
        )

        reference_data = ref_data.loc[:, columns]

        # Generate and save reports
        LOGGER.info("Create a model performance report")
        model_performance_report = Report(metrics=[RegressionQualityMetric()])
        model_performance_report.run(
            reference_data=reference_data,
            current_data=current_data,
            column_mapping=COLUMN_MAPPING,
        )

        LOGGER.info("Target drift report")
        target_drift_report = Report(metrics=[ColumnDriftMetric(COLUMN_MAPPING.target)])
        target_drift_report.run(
            reference_data=reference_data,
            current_data=current_data,
            column_mapping=COLUMN_MAPPING,
        )

        LOGGER.info("Save metrics to database")
        commit_model_metrics_to_db(
            model_performance_report=model_performance_report.as_dict(),
            target_drift_report=target_drift_report.as_dict(),
            timestamp=ts.timestamp(),
            db_uri=MONITORING_DB_URI,
        )

        LOGGER.info("Save HTML report if Target Drift detected")
        target_drift = detect_target_drift(target_drift_report)
        path = Path(f"{TARGET_DRIFT_REPORTS_DIR}/{ts.to_datetime_string()}.html")
        if target_drift:
            target_drift_report.save_html(path)

    LOGGER.info("Complete the pipeline")


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--ts", dest="ts", required=True)
    args_parser.add_argument(
        "--interval", dest="interval", required=False, type=int, default=60
    )
    args = args_parser.parse_args()

    ts = pendulum.parse(args.ts)
    monitor_model(ts=ts, interval=args.interval)
