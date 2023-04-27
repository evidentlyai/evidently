from typing import Text
from typing import Tuple

import pandas as pd
import pendulum


def get_batch_interval(ts: pendulum.DateTime, interval: int) -> Tuple[Text, Text]:
    """Get data batch for an interval.

    Args:
        ts (pendulum.DateTime): Timestamp.
        interval (int): Interval in minutes.

    Returns:
        Tuple[Text, Text]:
            Tuple of start and end time.
    """

    batch_start_time = ts.subtract(minutes=interval)

    # Convert to 'datetime' format
    ts = ts.to_datetime_string()
    batch_start_time = batch_start_time.to_datetime_string()

    start_time = batch_start_time
    end_time = ts
    print(start_time, end_time)

    return start_time, end_time


def extract_batch_data(
    data: pd.DataFrame, start_time: Text, end_time: Text
) -> pd.DataFrame:
    """Extract the batch data for specified time interval.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        start_time (Text): Start time.
        end_time (Text): End time.

    Returns:
        pd.DataFrame: Data batch - Pandas dataframe.
    """

    data = data.set_index("lpep_pickup_datetime")
    data = data.sort_index().loc[start_time:end_time]

    return data


def prepare_scoring_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare scoring data.

    Args:
        data (pd.DataFrame): Input data - Pandas dataframe.

    Returns:
        pd.DataFrame: Pandas dataframe with specific features (columns).
    """

    # Define the target variable, numerical features, and categorical features
    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["PULocationID", "DOLocationID"]
    data = data.loc[:, num_features + cat_features]

    return data
