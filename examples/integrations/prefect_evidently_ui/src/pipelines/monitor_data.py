import argparse
import logging
from pathlib import Path
from typing import List, Text

import pandas as pd
import pendulum
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import DatasetDriftMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.report import Report
from evidently.ui.workspace import Workspace
from prefect import flow, task

from config.evidently_config import EVIDENTLY_WS
from src.utils.evidently_monitoring import get_evidently_project
from src.utils.utils import extract_batch_data, get_batch_interval


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
    current_data = extract_batch_data(
        data,
        start_time=start_time,
        end_time=end_time
    )

    # Get predictions for the current data
    filename = pendulum.parse(end_time).to_date_string()
    path = Path(f"{PREDICTIONS_DIR}/{filename}.parquet")
    predictions = pd.read_parquet(path)

    # Merge current data with predictions
    current_data = current_data.merge(predictions, on="uuid", how="left")

    # Fill missing values
    current_data = current_data.fillna(current_data.median(numeric_only=True)).fillna(-1)

    return current_data


@task
def generate_data_quality_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    num_features: List[Text],
    prediction_col: Text,
    timestamp: float
) -> Report:
    """
    Generate data quality report.

    Args:
        current_data (pd.DataFrame):
            The current DataFrame with features and predictions.
        reference_data (pd.DataFrame):
            The reference DataFrame with features and predictions.
        num_features (List[Text]):
            List of numerical feature column names.
        prediction_col (Text):
            Name of the prediction column.
        timestamp (float):
            Metric pipeline execution timestamp.

    Returns:
        Report: Evidently data quality report.
    """

    logging.info("Prepare column mapping")
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = num_features
    column_mapping.prediction = prediction_col

    logging.info("Data quality report")
    data_quality_report = Report(
        metrics=[
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
        ],
        timestamp=pendulum.from_timestamp(timestamp)
    )
    data_quality_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    return data_quality_report


@task
def generate_prediction_drift_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    num_features: List[Text],
    prediction_col: Text,
    timestamp: float
) -> Report:
    """
    Generate prediction drift report.

    Args:
        current_data (pd.DataFrame):
            The current DataFrame with features and predictions.
        reference_data (pd.DataFrame):
            The reference DataFrame with features and predictions.
        num_features (List[Text]):
            List of numerical feature column names.
        prediction_col (Text):
            Name of the prediction column.
        timestamp (float):
            Metric pipeline execution timestamp.

    Returns:
        Report: Evidently prediction drift report.
    """

    logging.info("Prepare column mapping")
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = num_features
    column_mapping.prediction = prediction_col

    logging.info("Predictions drift report")
    prediction_drift_report = Report(
        metrics=[
            ColumnDriftMetric(column_name=prediction_col, stattest="wasserstein"),
            ColumnSummaryMetric(column_name=prediction_col),
        ],
        timestamp=pendulum.from_timestamp(timestamp)
    )
    prediction_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    return prediction_drift_report


@flow(flow_run_name="monitor-data-on-{ts}", log_prints=True)
def monitor_data(
    ts: pendulum.DateTime,
    interval: int = 60
) -> None:
    """Build and save data validation reports.

    Args:
        ts (pendulum.DateTime): Timestamp.
        interval (int, optional): Interval. Defaults to 60.
    """

    num_features = [
        "passenger_count", "trip_distance",
        "fare_amount", "total_amount"
    ]
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

        # Get Evidently workspace
        ws: Workspace = Workspace.create(EVIDENTLY_WS)

        # Data Quality (drift)
        data_quality_report = generate_data_quality_report(
            current_data=current_data,
            reference_data=reference_data,
            num_features=num_features,
            prediction_col=prediction_col,
            timestamp=ts.timestamp()
        )

        # Add reports (snapshots) to the Project Monitoring Dashboard
        project_dq = get_evidently_project(ws, "Data Quality")
        ws.add_report(project_dq.id, data_quality_report)

        # Predictions Drift
        pred_drift_report = generate_prediction_drift_report(
            current_data=current_data,
            reference_data=reference_data,
            num_features=num_features,
            prediction_col=prediction_col,
            timestamp=ts.timestamp()
        )
        project_pd = get_evidently_project(ws, "Predictions Drift")
        ws.add_report(project_pd.id, pred_drift_report)


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--ts",
        dest="ts",
        required=True
    )
    args_parser.add_argument(
        "--interval",
        dest="interval",
        required=False,
        default=60
    )
    args = args_parser.parse_args()

    ts = pendulum.parse(args.ts)
    monitor_data(ts=ts, interval=args.interval)
