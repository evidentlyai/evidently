from pathlib import Path

import joblib
import pandas as pd
from src.utils.utils import prepare_scoring_data


def prepare_reference_dataset():
    """Prepare reference dataset for the monitoring"""

    DATA_FEATURES_DIR = "data/features"
    target_col = "duration_min"
    prediction_col = "predictions"

    print("Load data")
    path = f"{DATA_FEATURES_DIR}/green_tripdata_2021-01.parquet"
    data = pd.read_parquet(path)
    data = data.sample(frac=0.3)
    clean_data = data.fillna(data.median())
    scoring_data = prepare_scoring_data(clean_data)

    print("Load model")
    model = joblib.load("models/model.joblib")

    print("Predictions generation")
    predictions_df = data.loc[:, ["uuid", target_col]]
    predictions_df[prediction_col] = model.predict(scoring_data)

    print("Save reference dataset")
    REFERENCE_DATA_DIR = Path("data/reference")
    REFERENCE_DATA_DIR.mkdir(exist_ok=True)
    path = REFERENCE_DATA_DIR / "reference_data_2021-01.parquet"

    df = pd.concat([predictions_df, scoring_data], axis=1)
    df.to_parquet(path)


if __name__ == "__main__":

    prepare_reference_dataset()
