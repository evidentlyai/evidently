import pandas as pd
import uuid


def process() -> None:
    """
    Process given dataset:
    - add column "uuid" and generate values
    - calculate column "duration_min"
    - fill missing values
    - drop rows where "duration_min" less then 1
    """

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
        data["duration_min"] = (
            data.lpep_dropoff_datetime - data.lpep_pickup_datetime
        )
        data.duration_min = data.duration_min.apply(
            lambda td: float(td.total_seconds() / 60)
        )

        # Drop unused columns
        data = data.drop(["store_and_fwd_flag"], axis=1)

        # Fill missing values with the median for numeric columns only
        numeric_columns = data.select_dtypes(include="number").columns
        medians = data[numeric_columns].median()
        data = data.fillna(medians).fillna(0)
        data = data[data['duration_min'] != 0]

        print("Save data")
        path_destination = f"{DATA_FEATURES_DIR}/{file}"
        data.to_parquet(path_destination)


if __name__ == "__main__":

    process()
