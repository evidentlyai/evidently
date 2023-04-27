import argparse
import logging
import time
from pathlib import Path
from typing import Dict
from typing import List
from typing import Text

import pandas as pd
import pendulum
from prefect import flow
from prefect import task
from src.monitoring.data_quality import commit_data_metrics_to_db
from src.utils.utils import extract_batch_data
from src.utils.utils import get_batch_interval

from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetSummaryMetric
from evidently.report import Report


@task
def prepare_current_data(start_time: Text, end_time: Text) -> pd.DataFrame:
    """Merge the current data with the corresponding predictions.

    Args:
        start_time (Text): Start time.
        end_time (Text): End time.

    Returns:
        pd.DataFrame:
            A DataFrame containing the current data merged with predictions.
    """

    DATA_FEATURES_DIR = "data/features"
    PREDICTIONS_DIR = "data/predictions"

    # Get current data (features)
    data_path = f"{DATA_FEATURES_DIR}/green_tripdata_2021-02.parquet"
    data = pd.read_parquet(data_path)
    current_data = extract_batch_data(data, start_time=start_time, end_time=end_time)

    # Get predictions for the current data
    filename = pendulum.parse(end_time).to_date_string()
    path = Path(f"{PREDICTIONS_DIR}/{filename}.parquet")
    predictions = pd.read_parquet(path)

    # Merge current data with predictions
    current_data = current_data.merge(predictions, on="uuid", how="left")

    # Fill missing values
    current_data = current_data.fillna(current_data.median()).fillna(-1)

    return current_data


@task
def generate_reports(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    num_features: List[Text],
    cat_features: List[Text],
    prediction_col: Text,
    timestamp: float,
) -> None:
    """
    Generate data quality and data drift reports and
    commit metrics to the database.

    Args:
        current_data (pd.DataFrame):
            The current DataFrame with features and predictions.
        reference_data (pd.DataFrame):
            The reference DataFrame with features and predictions.
        num_features (List[Text]):
            List of numerical feature column names.
        cat_features (List[Text]):
            List of categorical feature column names.
        prediction_col (Text):
            Name of the prediction column.
        timestamp (float):
            Metric pipeline execution timestamp.
    """

    logging.info("Prepare column mapping")
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = num_features
    column_mapping.prediction = prediction_col

    # if current_data.predictions.notnull().sum() > 0:
    #     column_mapping.prediction = prediction_col

    logging.info("Data quality report")
    data_quality_report = Report(metrics=[DatasetSummaryMetric()])
    data_quality_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    logging.info("Data drift report")
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    logging.info("Commit metrics into database")
    data_quality_report_content: Dict = data_quality_report.as_dict()
    data_drift_report_content: Dict = data_drift_report.as_dict()
    commit_data_metrics_to_db(
        data_quality_report=data_quality_report_content,
        data_drift_report=data_drift_report_content,
        timestamp=timestamp,
    )


@flow(flow_run_name="monitor-data-on-{ts}", log_prints=True)
def monitor_data(ts: pendulum.DateTime, interval: int = 60) -> None:
    """Build and save data validation reports.

    Args:
        ts (pendulum.DateTime): Timestamp.
        interval (int, optional): Interval. Defaults to 60.
    """

    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["PULocationID", "DOLocationID"]
    prediction_col = "predictions"

    # Prepare current data
    start_time, end_time = get_batch_interval(ts, interval)
    current_data: pd.DataFrame = prepare_current_data(start_time, end_time)

    # Prepare reference data
    DATA_REF_DIR = "data/reference"
    ref_path = f"{DATA_REF_DIR}/reference_data_2021-01.parquet"
    ref_data = pd.read_parquet(ref_path)
    columns: List[Text] = num_features + cat_features + [prediction_col]
    reference_data = ref_data.loc[:, columns]

    if current_data.shape[0] == 0:
        # Skip monitoring if current data is empty
        # Usually it may happen for few first batches
        print("Current data is empty!")
        print("Skip model monitoring")

    else:
        # Prepare column_mapping object
        # for Evidently reports and generate reports
        generate_reports(
            current_data=current_data,
            reference_data=reference_data,
            num_features=num_features,
            cat_features=cat_features,
            prediction_col=prediction_col,
            timestamp=ts.timestamp(),
        )


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--ts", dest="ts", required=True)
    args_parser.add_argument("--interval", dest="interval", required=False, default=60)
    args = args_parser.parse_args()

    ts = pendulum.parse(args.ts)
    monitor_data(ts=ts, interval=args.interval)
