import argparse
import logging
from typing import List, Text

import pandas as pd
import pendulum
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    RegressionQualityMetric,
    DatasetSummaryMetric
)
from evidently.report import Report
from evidently.metrics import ColumnSummaryMetric
from evidently.ui.workspace import Workspace
from prefect import flow, task

from config.evidently_config import EVIDENTLY_WS
from src.pipelines.monitor_data import prepare_current_data
from src.utils.evidently_monitoring import get_evidently_project
from src.utils.utils import get_batch_interval


@task
def generate_model_performance_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    num_features: List[Text],
    cat_features: List[Text],
    prediction_col: Text,
    target_col: Text,
    timestamp: float
) -> Report:
    """
    Generate model performance report.

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

    Returns:
        Report: Evidently model performance report.
    """

    print("Prepare column_mapping object for Evidently reports")
    column_mapping = ColumnMapping()
    column_mapping.target = target_col
    column_mapping.prediction = prediction_col
    column_mapping.numerical_features = num_features
    column_mapping.categorical_features = cat_features

    logging.info("Create a model performance report")
    model_performance_report = Report(
        metrics=[RegressionQualityMetric()],
        timestamp=pendulum.from_timestamp(timestamp)
    )
    model_performance_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    return model_performance_report


@task
def generate_target_drift_report(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    num_features: List[Text],
    cat_features: List[Text],
    prediction_col: Text,
    target_col: Text,
    timestamp: float
) -> Report:
    """
    Generate target drift report.

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

    Returns:
        Report: Evidently target drift report.
    """

    print("Prepare column_mapping object for Evidently reports")
    column_mapping = ColumnMapping()
    column_mapping.target = target_col
    column_mapping.prediction = prediction_col
    column_mapping.numerical_features = num_features
    column_mapping.categorical_features = cat_features

    logging.info("Target drift report")
    target_drift_report = Report(
        metrics=[
            ColumnDriftMetric(column_name=target_col, stattest="wasserstein"),
            ColumnSummaryMetric(column_name=target_col),
            DatasetSummaryMetric()
        ],
        timestamp=pendulum.from_timestamp(timestamp)
    )
    target_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    return target_drift_report


@flow(flow_run_name="monitor-model-on-{ts}", log_prints=True)
def monitor_model(
    ts: pendulum.DateTime,
    interval: int = 60
) -> None:
    """Build and save monitoring reports.

    Args:
        ts (pendulum.DateTime, optional): Timestamp.
        interval (int, optional): Interval. Defaults to 60.
    """

    DATA_REF_DIR = "data/reference"
    target_col = "duration_min"
    prediction_col = "predictions"
    num_features = [
        "passenger_count", "trip_distance",
        "fare_amount", "total_amount"
    ]
    cat_features = ["PULocationID", "DOLocationID"]

    # Prepare current data
    start_time, end_time = get_batch_interval(ts, interval)
    current_data = prepare_current_data(start_time, end_time)

    if current_data.shape[0] == 0:
        # Skip monitoring if current data is empty
        # Usually it may happen for few first batches
        print("Current data is empty!")
        print("Skip model monitoring")

    else:

        # Get Evidently workspace
        ws: Workspace = Workspace.create(EVIDENTLY_WS)

        # Prepare reference data
        ref_path = f"{DATA_REF_DIR}/reference_data_2021-01.parquet"
        ref_data = pd.read_parquet(ref_path)
        columns: List[Text] = (
            num_features + cat_features + [target_col, prediction_col]
        )
        reference_data = ref_data.loc[:, columns]

        # Model performance report
        model_performance_report = generate_model_performance_report(
            current_data=current_data,
            reference_data=reference_data,
            num_features=num_features,
            cat_features=cat_features,
            prediction_col=prediction_col,
            target_col=target_col,
            timestamp=ts.timestamp()
        )

        # Add reports (snapshots) to the Project Monitoring Dashboard
        project_mp = get_evidently_project(ws, "Model Performance")
        ws.add_report(project_mp.id, model_performance_report)

        target_drift_report = generate_target_drift_report(
            current_data=current_data,
            reference_data=reference_data,
            num_features=num_features,
            cat_features=cat_features,
            prediction_col=prediction_col,
            target_col=target_col,
            timestamp=ts.timestamp()
        )

        project_td = get_evidently_project(ws, "Target Drift")
        ws.add_report(project_td.id, target_drift_report)


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
    monitor_model(ts=ts, interval=args.interval)
