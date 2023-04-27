import argparse
from pathlib import Path
from typing import Text

import joblib
import pandas as pd
import pendulum

from prefect import flow, task
from src.utils.utils import (
    get_batch_interval,
    extract_batch_data,
    prepare_scoring_data
)


@task
def load_data(path: Path, start_time: Text, end_time: Text) -> pd.DataFrame:
    """Load data from parquet file.

    Args:
        path (Path): Path to data.
        start_time (Text): Start time.
        end_time (Text): End time.

    Returns:
        pd.DataFrame: Loaded Pandas dataframe.
    """

    print(f'Data source: {path}')
    data = pd.read_parquet(path)

    print("Extract batch data")
    data = extract_batch_data(data, start_time=start_time, end_time=end_time)
    data = data.fillna(data.median()).fillna(0)

    return data


@task
def get_predictions(data: pd.DataFrame, model) -> pd.DataFrame:
    """Predictions generation.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        model (_type_): Model object.

    Returns:
        pd.DataFrame: Pandas dataframe with predictions column.
    """

    scoring_data = prepare_scoring_data(data)
    predictions = data[["uuid"]]
    predictions['predictions'] = model.predict(scoring_data)

    return predictions


@task
def save_predictions(predictions: pd.DataFrame, path: Path) -> None:
    """Save predictions to parquet file.

    Args:
        predictions (pd.DataFrame): Pandas dataframe with predictions column.
        path (Path): Path to save dataframe.
    """

    # Append data to existing file or, create a new one
    is_append = True if path.is_file() else False
    predictions.to_parquet(path, engine='fastparquet', append=is_append)
    print(f'Predictions saved to: {path}')


@flow(flow_run_name="predict-on-{ts}", log_prints=True)
def predict(
    ts: pendulum.DateTime,
    interval: int = 60
) -> None:
    """Calculate predictions for the new batch (interval) data.

    Args:
        ts (pendulum.DateTime, optional): Timestamp. Defaults to None.
        interval (int, optional): Interval. Defaults to 60.
    """

    DATA_FEATURES_DIR = 'data/features'

    # Compute the batch start and end time
    start_time, end_time = get_batch_interval(ts, interval)

    # Prepare data
    path = Path(f'{DATA_FEATURES_DIR}/green_tripdata_2021-02.parquet')
    batch_data = load_data(path, start_time, end_time)

    if batch_data.shape[0] > 0:

        # Predictions generation
        model = joblib.load('models/model.joblib')
        predictions: pd.DataFrame = get_predictions(batch_data, model)

        # Save predictions
        filename = ts.to_date_string()
        path = Path(f'data/predictions/{filename}.parquet')
        save_predictions(predictions, path)

    else:
        print("No data to predict")


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
    predict(ts=ts, interval=args.interval)
