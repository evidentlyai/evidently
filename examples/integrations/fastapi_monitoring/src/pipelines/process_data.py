import uuid

import pandas as pd


def process() -> None:
    """Train a linear regression model on the given dataset."""

    # Specify the raw data directory and read the January dataset
    DATA_RAW_DIR = "data/raw"
    DATA_FEATURES_DIR = "data/features"

    files = [
        "green_tripdata_2021-01.parquet",
        "green_tripdata_2021-02.parquet"
    ]

    print("Load train data")
    for file in files:

        path_source = f"{DATA_RAW_DIR}/{file}"
        data = pd.read_parquet(path_source)

        print("Generate UID")
        data["uuid"] = [uuid.uuid4() for x in range(len(data))]
        data["uuid"] = data["uuid"].astype("str")

        # Generate target variable (duration in minutes)
        dropoff_dt = data.lpep_dropoff_datetime
        pickup_dt = data.lpep_pickup_datetime
        data["duration_min"] = dropoff_dt - pickup_dt
        data.duration_min = data.duration_min.apply(
            lambda td: float(td.total_seconds() / 60)
        )

        # Drop unused columns
        data = data.drop(["store_and_fwd_flag"], axis=1)

        # Fill missing values with the median for numeric columns only
        numeric_columns = data.select_dtypes(include='number').columns
        medians = data[numeric_columns].median()
        data = data.fillna(medians).fillna(0)
        data = data[data['duration_min'] != 0]

        print("Save data")
        path_destination = f"{DATA_FEATURES_DIR}/{file}"
        data.to_parquet(path_destination)


if __name__ == "__main__":

    process()
