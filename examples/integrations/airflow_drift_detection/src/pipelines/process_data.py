import uuid

import pandas as pd

from config import DATA_FILES, DATA_RAW_DIR, FEATURES_DIR


def process() -> None:
    """Process a dataset and save it as a feature dataset"""

    # Specify the raw data directory and read the January dataset
    print("Load train data")
    for file in DATA_FILES:

        path_source = f"{DATA_RAW_DIR}/{file}"
        data = pd.read_parquet(path_source)

        print("Generate UID")
        data["uuid"] = [uuid.uuid4() for x in range(len(data))]
        data["uuid"] = data["uuid"].astype("str")

        # Generate target variable (duration in minutes)
        data["duration_min"] = data.lpep_dropoff_datetime - data.lpep_pickup_datetime
        data.duration_min = data.duration_min.apply(
            lambda td: float(td.total_seconds() / 60)
        )

        # Drop unused columns
        data = data.drop(["store_and_fwd_flag"], axis=1)

        # Fill missing values with the median for numeric columns only
        numeric_columns = data.select_dtypes(include="number").columns
        medians = data[numeric_columns].median()
        data = data.fillna(medians).fillna(0)
        data = data[data["duration_min"] != 0]

        print("Save data")
        path_destination = f"{FEATURES_DIR}/{file}"
        data.to_parquet(path_destination)


if __name__ == "__main__":

    process()
