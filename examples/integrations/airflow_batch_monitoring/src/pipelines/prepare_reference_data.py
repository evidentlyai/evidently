from pathlib import Path

import joblib
import pandas as pd
from config import FEATURES_DIR
from config import REFERENCE_DIR
from src.utils.utils import prepare_scoring_data


def prepare_reference_dataset():
    """Prepare a reference dataset for the monitoring"""

    target_col = "duration_min"
    prediction_col = "predictions"

    print("Load data")
    path = f"{FEATURES_DIR}/green_tripdata_2021-01.parquet"
    data = pd.read_parquet(path)
    data = data.sample(frac=0.3)
    clean_data = data.fillna(data.median(numeric_only=True))
    scoring_data = prepare_scoring_data(clean_data)

    print("Load model")
    model = joblib.load("models/model.joblib")

    print("Predictions generation")
    predictions_df = data.loc[:, ["uuid", target_col]]
    predictions_df[prediction_col] = model.predict(scoring_data)

    print("Save reference dataset")
    reference_dir = Path(REFERENCE_DIR)
    reference_dir.mkdir(exist_ok=True)
    path = reference_dir / "reference_data_2021-01.parquet"

    df = pd.concat([predictions_df, scoring_data], axis=1)
    df.to_parquet(path)


if __name__ == "__main__":

    prepare_reference_dataset()
